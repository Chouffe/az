(ns webapp.db.abdatapoints
  (:require [monger.collection :as mc]
            [monger.operators :as mo]
            [clj-time.core :as time]
            [webapp.db.component :as db]))

(defn get-by-uuid
  [uuid]
  (mc/find-maps db/db "abdatapoints" {:uuid uuid}))

(defn delete-by-uuid
  [uuid]
  (mc/remove db/db "abdatapoints" {:uuid uuid}))

(defn insert
  [uuid features result]
  (mc/insert db/db "abdatapoints" {:uuid uuid
                                   :features features
                                   :result result
                                   :time (time/now)}))
