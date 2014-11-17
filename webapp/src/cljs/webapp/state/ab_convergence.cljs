(ns webapp.state.ab-convergence
  (:require [reagent.core :as reagent])
  (:refer-clojure :exclude [get set]))

(defonce ab-convergence-ratom (reagent/atom {}))

(defn set
  [uuid data]
  ;; (reset! schema-ratom {uuid schema})
  (swap! ab-convergence-ratom assoc-in [(keyword uuid)] data))

(defn delete
  [uuid]
  (swap! ab-convergence-ratom dissoc (keyword uuid)))

(defn get
  [uuid]
  (get-in @ab-convergence-ratom [(keyword uuid)]))

