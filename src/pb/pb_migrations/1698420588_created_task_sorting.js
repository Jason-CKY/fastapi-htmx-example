/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const collection = new Collection({
    "id": "0hlmae0eymcgtr2",
    "created": "2023-10-27 15:29:48.082Z",
    "updated": "2023-10-27 15:29:48.082Z",
    "name": "task_sorting",
    "type": "base",
    "system": false,
    "schema": [
      {
        "system": false,
        "id": "utyfzwou",
        "name": "status",
        "type": "select",
        "required": false,
        "presentable": false,
        "unique": false,
        "options": {
          "maxSelect": 1,
          "values": [
            "backlog",
            "progress",
            "done"
          ]
        }
      },
      {
        "system": false,
        "id": "slg1phqw",
        "name": "sorting_order",
        "type": "json",
        "required": false,
        "presentable": false,
        "unique": false,
        "options": {}
      }
    ],
    "indexes": [],
    "listRule": null,
    "viewRule": null,
    "createRule": null,
    "updateRule": null,
    "deleteRule": null,
    "options": {}
  });

  return Dao(db).saveCollection(collection);
}, (db) => {
  const dao = new Dao(db);
  const collection = dao.findCollectionByNameOrId("0hlmae0eymcgtr2");

  return dao.deleteCollection(collection);
})
