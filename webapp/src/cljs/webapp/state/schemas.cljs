(ns webapp.state.schemas
  (:require [reagent.core :as reagent]
            [webapp.components :as components])
  (:refer-clojure :exclude [get set]))

(defonce schema-ratom (reagent/atom {}))

(defn set
  [{:keys [uuid features] :as schema}]
  ;; (reset! schema-ratom {uuid schema})
  (swap! schema-ratom assoc-in [(keyword uuid)] schema))

(defn get
  [uuid]
  (get-in @schema-ratom [(keyword uuid)]))

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
