(ns webapp.state.convergence
  (:require [reagent.core :as reagent])
  (:refer-clojure :exclude [get set]))

(defonce convergence-ratom (reagent/atom {}))

(defn set
  [uuid data]
  (swap! convergence-ratom assoc-in [(keyword uuid)] data))

(defn delete
  [uuid]
  (swap! convergence-ratom dissoc (keyword uuid)))

(defn get
  [uuid]
  (get-in @convergence-ratom [(keyword uuid)]))
