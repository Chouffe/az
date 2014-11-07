(ns webapp.home
  (:require [reagent.core :as reagent]
            [webapp.state.schemas :as schemas]
            [webapp.state.application :as application]
            [webapp.components :as components]
            [webapp.routes :as routes]
            [figwheel.client :as fw :include-macros true]))

(defn home-comp
  []
  [:div.container
   [:div "HELLO"]])
