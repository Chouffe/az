(ns webapp.state.cost-function
  (:require [reagent.core :as reagent])
  (:refer-clojure :exclude [get set]))

(defonce cost-function-ratom (reagent/atom {}))

(defn set
  [uuid data]
  ;; (reset! schema-ratom {uuid schema})
  (swap! cost-function-ratom assoc-in [(keyword uuid)] data))

(defn get
  [uuid]
  (get-in @cost-function-ratom [(keyword uuid)]))

