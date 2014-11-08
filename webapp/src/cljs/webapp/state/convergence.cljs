(ns webapp.state.convergence
  (:require [reagent.core :as reagent])
  (:refer-clojure :exclude [get set]))

(defonce convergence-ratom (reagent/atom {}))

(defn set
  [uuid data]
  ;; (reset! schema-ratom {uuid schema})
  (swap! convergence-ratom assoc-in [(keyword uuid)] data))

(defn get
  [uuid]
  (get-in @convergence-ratom [(keyword uuid)]))
