const { DynamoDBClient } = require('@aws-sdk/client-dynamodb');
const { DynamoDBDocumentClient, PutCommand } = require('@aws-sdk/lib-dynamodb');
const { v4: uuidv4 } = require('uuid');

// Initialize DynamoDB client with explicit region
const client = new DynamoDBClient({ region: 'eu-central-1' });
const dynamoDB = DynamoDBDocumentClient.from(client);
const TABLE_NAME = 'cmtr-5f9b79e5-Events'; // Hardcoded table name with prefix

exports.handler = async (event) => {
  console.log("Event received:", JSON.stringify(event, null, 2));
  
  try {
    // Parse the request body if needed
    const requestBody = event.body ? JSON.parse(event.body) : event;
    
    // Validate required fields
    if (!requestBody.principalId || !requestBody.content) {
      return {
        statusCode: 400,
        body: JSON.stringify({
          message: 'Missing required fields: principalId or content'
        })
      };
    }
    
    // Create the event object
    const newEvent = {
      id: uuidv4(),
      principalId: requestBody.principalId,
      createdAt: new Date().toISOString(),
      body: requestBody.content
    };
    
    console.log("Saving to DynamoDB table:", TABLE_NAME);
    console.log("Item:", JSON.stringify(newEvent, null, 2));
    
    // Save to DynamoDB
    await dynamoDB.send(new PutCommand({
      TableName: TABLE_NAME,
      Item: newEvent
    }));
    
    // Return success response in the required format
    return {
      statusCode: 201,
      body: JSON.stringify({
        statusCode: 201,
        event: newEvent
      })
    };
  } catch (error) {
    console.error("Error:", error);
    
    return {
      statusCode: 500,
      body: JSON.stringify({
        message: 'Internal server error',
        error: error.message
      })
    };
  }
};