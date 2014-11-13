(ns webapp.db.component
  (:require [com.stuartsierra.component :as component]
            [monger.core :as mg]
            [webapp.utils.logging :as log]))

(defrecord DatabaseComponent [db conn]
  component/Lifecycle
  (start [this]
    (log/info "Starting Database connection")
    (let [conn (mg/connect)
          db (mg/get-db conn "az")]
      ;; Hack
      (def conn conn)
      (def db db)
      (assoc this :db db :conn conn)))
  (stop [this]
    (log/info "Stopping database connection")
    (mg/disconnect (:conn this))
    (dissoc this :db :conn)))

(defn db-component
  []
  (map->DatabaseComponent {}))
