const AWS = require("aws-sdk");
const { v4: uuidv4 } = require("uuid");

const dynamodb = new AWS.DynamoDB.DocumentClient();

const AUDIT_TABLE = process.env.AUDIT_TABLE;

exports.handler = async (event) => {
  const records = event.Records || [];

  console.log("AUDIT_TABLE", AUDIT_TABLE);

  // Loop through the records
  for (const record of records) {
    if (record.eventName !== "INSERT" && record.eventName !== "MODIFY") {
      continue; // Only care about new/updated items
    }

    const newItem = AWS.DynamoDB.Converter.unmarshall(
      record.dynamodb.NewImage || {}
    );
    const oldItem = AWS.DynamoDB.Converter.unmarshall(
      record.dynamodb.OldImage || {}
    );

    // Constructing the audit entry
    const auditEntry = {
      id: uuidv4(),
      principalId: newItem.principalId || "unknown", // Add the principalId
      createdAt: new Date().toISOString(), // Add createdAt
      body: newItem, // Assuming the 'body' is the newItem
      itemKey: newItem.key,
      modificationTime: new Date().toISOString(),
    };

    // If the event is INSERT, add the new value
    if (record.eventName === "INSERT") {
      auditEntry.newValue = newItem;
    } else if (record.eventName === "MODIFY") {
      const changes = {};
      if (oldItem.value !== newItem.value) {
        changes.updatedAttribute = "value";
        changes.oldValue = oldItem.value;
        changes.newValue = newItem.value;
      }

      Object.assign(auditEntry, changes);
    }

    // Save the audit entry to DynamoDB
    try {
      await dynamodb
        .put({
          TableName: AUDIT_TABLE,
          Item: auditEntry,
        })
        .promise();
    } catch (error) {
      console.error("Error saving audit entry to DynamoDB:", error);
      throw new Error("Error saving audit entry to DynamoDB");
    }
  }

  // Return a proper response with statusCode 201
  return {
    statusCode: 201,
    body: JSON.stringify({ message: "Audit entry created successfully" }),
  };
};
