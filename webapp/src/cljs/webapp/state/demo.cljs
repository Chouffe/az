(ns webapp.state.demo
  (:require [reagent.core :as reagent]))

(defonce test-uuid->tab-ratom (reagent/atom {}))

(defn set-tab
  [uuid tab]
  (swap! test-uuid->tab-ratom assoc-in [uuid] tab))

(defn get-tab
  [uuid]
  (get @test-uuid->tab-ratom uuid))

(defonce uuid-ratom (reagent/atom nil))

(defn set-uuid
  [uuid]
  (reset! uuid-ratom uuid))

(defn get-uuid
  []
  @uuid-ratom)
