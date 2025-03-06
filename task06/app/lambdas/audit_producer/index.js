const AWS = require("aws-sdk");
const { v4: uuidv4 } = require("uuid");

const dynamodb = new AWS.DynamoDB.DocumentClient();

const AUDIT_TABLE = process.env.AUDIT_TABLE;

exports.handler = async (event) => {
  const records = event.Records || [];

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

    const auditEntry = {
      id: uuidv4(),
      itemKey: newItem.key,
      modificationTime: new Date().toISOString(),
    };

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

    await dynamodb
      .put({
        TableName: AUDIT_TABLE,
        Item: auditEntry,
      })
      .promise();
  }

  return { status: "success" };
};
