# 📌 911 Operations Application - MongoDB Collections & Queries

## 1️⃣ User Management (`users` Collection)

| Operation               | MongoDB Query                                                       |
| ----------------------- | ------------------------------------------------------------------- |
| **Register User**       | `db.users.insertOne({...})`                                         |
| **Get User Profile**    | `db.users.findOne({ _id: ObjectId("user_id") })`                    |
| **Update User Profile** | `db.users.updateOne({ _id: ObjectId("user_id") }, { $set: {...} })` |
| **Delete User**         | `db.users.deleteOne({ _id: ObjectId("user_id") })`                  |

---

## 2️⃣ Emergency Calls (`calls` Collection)

| Operation              | MongoDB Query                                                                         |
| ---------------------- | ------------------------------------------------------------------------------------- |
| **Log a Call**         | `db.calls.insertOne({...})`                                                           |
| **Get Call Details**   | `db.calls.findOne({ _id: ObjectId("call_id") })`                                      |
| **List All Calls**     | `db.calls.find({})`                                                                   |
| **Update Call Status** | `db.calls.updateOne({ _id: ObjectId("call_id") }, { $set: {status: "in-progress"} })` |
| **Delete Call Record** | `db.calls.deleteOne({ _id: ObjectId("call_id") })`                                    |

---

## 3️⃣ Incident Management (`incidents` Collection)

| Operation                  | MongoDB Query                                                                              |
| -------------------------- | ------------------------------------------------------------------------------------------ |
| **Report an Incident**     | `db.incidents.insertOne({...})`                                                            |
| **Get Incident Details**   | `db.incidents.findOne({ _id: ObjectId("incident_id") })`                                   |
| **List All Incidents**     | `db.incidents.find({})`                                                                    |
| **Update Incident Status** | `db.incidents.updateOne({ _id: ObjectId("incident_id") }, { $set: {status: "resolved"} })` |
| **Delete Incident**        | `db.incidents.deleteOne({ _id: ObjectId("incident_id") })`                                 |

---

## 4️⃣ Dispatching & Responder Assignment (`dispatch` Collection)

| Operation                  | MongoDB Query                                                                              |
| -------------------------- | ------------------------------------------------------------------------------------------ |
| **Assign Responders**      | `db.dispatch.insertOne({...})`                                                             |
| **Get Dispatch Details**   | `db.dispatch.findOne({ _id: ObjectId("dispatch_id") })`                                    |
| **List Active Dispatches** | `db.dispatch.find({ status: "active" })`                                                   |
| **Update Dispatch Status** | `db.dispatch.updateOne({ _id: ObjectId("dispatch_id") }, { $set: {status: "completed"} })` |
| **Cancel Dispatch**        | `db.dispatch.deleteOne({ _id: ObjectId("dispatch_id") })`                                  |

---

## 5️⃣ Service Centers (`service_centers` Collection)

| Operation                           | MongoDB Query                                                                   |
| ----------------------------------- | ------------------------------------------------------------------------------- |
| **Add a Service Center**            | `db.service_centers.insertOne({...})`                                           |
| **Find Nearest Service Center**     | `db.service_centers.find({ location: { $near: [lat, lng] } })`                  |
| **Get Service Centers by Category** | `db.service_centers.find({ category: "hospital" })`                             |
| **Update Service Center Details**   | `db.service_centers.updateOne({ _id: ObjectId("center_id") }, { $set: {...} })` |
| **Remove a Service Center**         | `db.service_centers.deleteOne({ _id: ObjectId("center_id") })`                  |

---

## 6️⃣ SOS Requests (`sos_requests` Collection)

| Operation                 | MongoDB Query                                                                              |
| ------------------------- | ------------------------------------------------------------------------------------------ |
| **Trigger an SOS**        | `db.sos_requests.insertOne({...})`                                                         |
| **Get SOS Requests**      | `db.sos_requests.find({ user_id: "12345" })`                                               |
| **Update SOS Status**     | `db.sos_requests.updateOne({ _id: ObjectId("sos_id") }, { $set: {status: "responding"} })` |
| **Delete an SOS Request** | `db.sos_requests.deleteOne({ _id: ObjectId("sos_id") })`                                   |

---

## 7️⃣ Location Tracking (`locations` Collection)

| Operation                | MongoDB Query                                                                        |
| ------------------------ | ------------------------------------------------------------------------------------ |
| **Store User Location**  | `db.locations.insertOne({...})`                                                      |
| **Get Nearby Users**     | `db.locations.find({ location: { $near: [lat, lng] } })`                             |
| **Update Location**      | `db.locations.updateOne({ user_id: "12345" }, { $set: {lat: 37.77, lng: -122.41} })` |
| **Delete Location Data** | `db.locations.deleteOne({ user_id: "12345" })`                                       |

---

## 8️⃣ Notifications & Alerts (`notifications` Collection)

| Operation                     | MongoDB Query                                                                           |
| ----------------------------- | --------------------------------------------------------------------------------------- |
| **Send Notification**         | `db.notifications.insertOne({...})`                                                     |
| **Get User Notifications**    | `db.notifications.find({ user_id: "12345" })`                                           |
| **Mark Notification as Read** | `db.notifications.updateOne({ _id: ObjectId("notif_id") }, { $set: {status: "read"} })` |
| **Delete Notification**       | `db.notifications.deleteOne({ _id: ObjectId("notif_id") })`                             |

---

## 9️⃣ Community Safety Reports (`community_reports` Collection)

| Operation                   | MongoDB Query                                                                                    |
| --------------------------- | ------------------------------------------------------------------------------------------------ |
| **Submit a Safety Report**  | `db.community_reports.insertOne({...})`                                                          |
| **Get Reports by Location** | `db.community_reports.find({ location: { $near: [lat, lng] } })`                                 |
| **Update Report Status**    | `db.community_reports.updateOne({ _id: ObjectId("report_id") }, { $set: {status: "verified"} })` |
| **Delete a Report**         | `db.community_reports.deleteOne({ _id: ObjectId("report_id") })`                                 |

---

## 🔟 Feedback & Ratings (`feedback` Collection)

| Operation                      | MongoDB Query                                                                    |
| ------------------------------ | -------------------------------------------------------------------------------- |
| **Submit Feedback**            | `db.feedback.insertOne({...})`                                                   |
| **Get Feedback for a Service** | `db.feedback.find({ service_id: "hospital_123" })`                               |
| **Update Feedback**            | `db.feedback.updateOne({ _id: ObjectId("feedback_id") }, { $set: {rating: 5} })` |
| **Delete Feedback**            | `db.feedback.deleteOne({ _id: ObjectId("feedback_id") })`                        |

---

### 🚀 **Notes & Optimization Suggestions**

- **Indexing:** Use indexes for fast searches (`location`, `status`, `user_id`).
- **GeoSpatial Queries:** Use MongoDB's `$geoNear` for real-time location tracking.
- **Aggregation Pipelines:** Optimize reports and statistics retrieval.
- **TTL (Time-to-Live) Index:** Auto-delete old incident reports after a set period.
