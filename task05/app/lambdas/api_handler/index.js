const {
  DynamoDBClient,
  ListTablesCommand,
} = require("@aws-sdk/client-dynamodb");
const { DynamoDBDocumentClient, PutCommand } = require("@aws-sdk/lib-dynamodb");
const { v4: uuidv4 } = require("uuid");

// Initialize DynamoDB client
const client = new DynamoDBClient({ region: "eu-central-1" });
const dynamoDB = DynamoDBDocumentClient.from(client);

// Function to find the Events table
async function findEventsTable() {
  const { TableNames } = await client.send(new ListTablesCommand({}));
  console.log("Available tables:", TableNames);

  // Look for a table that contains 'Events' in its name
  const eventsTable = TableNames.find((name) => name.includes("Events"));
  if (!eventsTable) {
    throw new Error("Events table not found");
  }

  console.log("Found Events table:", eventsTable);
  return eventsTable;
}

exports.handler = async (event) => {
  console.log("Event received:", JSON.stringify(event, null, 2));

  try {
    // Find the Events table
    const TABLE_NAME = process.env.TARGET_TABLE || (await findEventsTable());
    console.log("Using table:", TABLE_NAME);

    // Parse the request body if needed
    const requestBody = event.body ? JSON.parse(event.body) : event;

    // Rest of your code...
    const newEvent = {
      id: uuidv4(),
      principalId: requestBody.principalId,
      createdAt: new Date().toISOString(),
      body: requestBody.content,
    };

    // Save to DynamoDB
    await dynamoDB.send(
      new PutCommand({
        TableName: TABLE_NAME,
        Item: newEvent,
      })
    );

    // Return response
    return {
      statusCode: 201,
      body: JSON.stringify({
        statusCode: 201,
        event: newEvent,
      }),
    };
  } catch (error) {
    console.error("Error:", error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        message: "Internal server error",
        error: error.message,
      }),
    };
  }
};
