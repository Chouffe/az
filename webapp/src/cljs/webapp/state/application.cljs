(ns webapp.state.application
  (:require [reagent.core :as reagent])
  (:refer-clojure :exclude [get set]))

(defonce tab-ratom (reagent/atom nil))

(defn set-tab
  [tab]
  (reset! tab-ratom tab))

(defn get-tab
  []
  @tab-ratom)

