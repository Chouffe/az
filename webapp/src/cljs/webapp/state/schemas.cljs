(ns webapp.state.schemas
  (:require [reagent.core :as reagent])
  (:refer-clojure :exclude [get set]))

(defonce schema-ratom (reagent/atom {}))

(defn set
  [{:keys [uuid features] :as schema}]
  (swap! schema-ratom assoc-in [(keyword uuid)] schema))

(defn get
  ([] (mapv second @schema-ratom))
  ([uuid] (get-in @schema-ratom [(keyword uuid)])))

(defn delete
  [uuid]
  (swap! schema-ratom dissoc (keyword uuid)))

(defn add-feature
  [uuid feature-name feature-map]
  (set (assoc-in (get uuid)
                 [:features (keyword feature-name)]
                 feature-map)))

(defn delete-feature
  [uuid feature-name]
  (let [schema (get uuid)
        new-features (dissoc (:features schema) (keyword feature-name))]
    (set (assoc schema :features new-features))))
