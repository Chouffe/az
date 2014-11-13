(ns webapp.db.datapoints
  (:require [monger.collection :as mc]
            [monger.operators :as mo]
            [clj-time.core :as time]
            [webapp.db.component :as db]))

(defn get-by-uuid
  [uuid]
  (mc/find-maps db/db "datapoints" {:uuid uuid}))

(defn delete-by-uuid
  [uuid]
  (mc/remove db/db "datapoints" {:uuid uuid}))

(defn insert
  [uuid features result]
  (mc/insert db/db "datapoints" {:uuid uuid
                                 :features features
                                 :result result
                                 :time (time/now)}))
