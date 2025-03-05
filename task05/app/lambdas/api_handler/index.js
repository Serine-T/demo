const { DynamoDBClient, PutItemCommand } = require("@aws-sdk/client-dynamodb");
const { v4: uuidv4 } = require("uuid");

// Environment variable injected via Syndicate aliases (syndicate_aliases.yml)
const TABLE_NAME = process.env.TARGET_TABLE || "Events";

const dynamoDbClient = new DynamoDBClient();

exports.handler = async (event) => {
    try {
        const body = JSON.parse(event.body);

        const principalId = body.principalId;
        const content = body.content;

        if (typeof principalId !== 'number' || !content || typeof content !== 'object') {
            return {
                statusCode: 400,
                body: JSON.stringify({ message: "Invalid request body" }),
            };
        }

        const createdAt = new Date().toISOString();
        const id = uuidv4();

        const dynamoItem = {
            id: { S: id },
            principalId: { N: principalId.toString() },
            createdAt: { S: createdAt },
            body: { S: JSON.stringify(content) }
        };

        const command = new PutItemCommand({
            TableName: TABLE_NAME,
            Item: dynamoItem,
        });

        await dynamoDbClient.send(command);

        const savedEvent = {
            id,
            principalId,
            createdAt,
            body: content,
        };

        return {
            statusCode: 201,
            body: JSON.stringify({ statusCode: 201, event: savedEvent }),
        };
    } catch (error) {
        console.error("Error handling event:", error);
        return {
            statusCode: 500,
            body: JSON.stringify({ message: "Internal server error" }),
        };
    }
};
