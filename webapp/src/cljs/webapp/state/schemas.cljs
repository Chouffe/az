(ns webapp.state.schemas
  (:require [reagent.core :as reagent])
  (:refer-clojure :exclude [get set]))

(defonce schema-ratom (reagent/atom {}))

(defn set
  [{:keys [uuid features] :as schema}]
  ;; (reset! schema-ratom {uuid schema})
  (swap! schema-ratom assoc-in [(keyword uuid)] schema))

(defn get
  [uuid]
  (get-in @schema-ratom [(keyword uuid)]))

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

(set
  {:uuid "test"
   :features {"a1" {:distribution "uniform"
                    :default 0
                    :params {"high" 0
                             "low" 1}}
              "a0" {:distribution "uniform"
                    :default 0
                    :params {"high" 0
                             "low" 1}}
              "a2" {:distribution "uniform"
                    :default 0
                    :params {"high" 0
                             "low" 1}}
              "a3" {:distribution "uniform"
                    :default 0
                    :params {"high" 0
                             "low" 1}}
              }})
