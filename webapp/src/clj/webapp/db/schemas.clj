(ns webapp.db.schemas
  (:require [monger.collection :as mc]
            [monger.operators :as mo]
            [webapp.db.component :as db]))

(defn get-all
  []
  (mc/find-maps db/db "schemas" {}))

(defn get-by-uuid
  [uuid]
  (mc/find-one-as-map db/db "schemas" {:uuid uuid}))

(defn remove-by-uuid
  [uuid]
  (mc/remove db/db "schemas" {:uuid uuid}))
