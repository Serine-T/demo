const { DynamoDBClient } = require("@aws-sdk/client-dynamodb");
const { DynamoDBDocumentClient, PutCommand } = require("@aws-sdk/lib-dynamodb");
const { v4: uuidv4 } = require("uuid");

// Initialize DynamoDB client with explicit region
const client = new DynamoDBClient({ region: "eu-central-1" });
const dynamoDB = DynamoDBDocumentClient.from(client);
const TABLE_NAME = process.env.TARGET_TABLE;
exports.handler = async (event) => {
  console.log("Event received:", JSON.stringify(event, null, 2));
  console.log("Resolved TABLE_NAME:", TABLE_NAME);

  try {
    // Parse the request body if needed
    const requestBody = event.body ? JSON.parse(event.body) : event;

    // Validate required fields
    if (!requestBody.principalId || !requestBody.content) {
      return {
        statusCode: 400,
        body: JSON.stringify({
          message: "Missing required fields: principalId or content",
        }),
      };
    }

    // Create the event object with the exact format required
    const newEvent = {
      id: uuidv4(),
      principalId: requestBody.principalId,
      createdAt: new Date().toISOString(),
      body: requestBody.content,
    };

    console.log("Saving to DynamoDB table:", TABLE_NAME);
    console.log("Item:", JSON.stringify(newEvent, null, 2));

    // Save to DynamoDB
    await dynamoDB.send(
      new PutCommand({
        TableName: TABLE_NAME,
        Item: newEvent,
      })
    );

    // Return the response in the EXACT format required
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
