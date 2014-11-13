(ns webapp.db.features
  (:require [monger.collection :as mc]
            [monger.operators :as mo]
            [webapp.db.component :as db]
            [webapp.db.schemas :as db-schemas]))

(defn add-feature
  [uuid feature-map]
  (when-let [{:keys [features] :as current-schema} (db-schemas/get-by-uuid uuid)]
    (let [new-features (merge features feature-map) ]
      (mc/update
        db/db "schemas" {:uuid uuid} {mo/$set {:features new-features}}))))

(defn remove-feature
  [uuid feature-name]
  (when-let [{:keys [features] :as current-schema} (db-schemas/get-by-uuid uuid)]
    (let [new-features (dissoc features (keyword feature-name))]
      (mc/update
        db/db "schemas" {:uuid uuid} {mo/$set {:features new-features}}))))
