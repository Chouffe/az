(ns webapp.core
  (:require [reagent.core :as reagent]
            [webapp.state.schemas :as schemas]
            [webapp.state.application :as application]
            [webapp.components :as components]
            [webapp.routes :as routes]
            [figwheel.client :as fw :include-macros true]
            [webapp.utils.ajax :as ajaxu]
            webapp.home
            webapp.demo
            webapp.experiments
            [cljs-http.client :as http]
            [cljs.core.async :refer [<!]])
  (:require-macros [cljs.core.async.macros :refer [go]]))


(enable-console-print!)

;; TEST
;; TODO: kill
(go
(let [response (<! (ajaxu/get-json "http://localhost:5002/api/lp2"))]
  (println response)))

(def tab->page
  {:home webapp.home/home-comp
   :experiments webapp.experiments/experiments-comp
   :experiment-results webapp.experiments/experiment-results-comp
   :demo-results webapp.demo/demo-results-comp})

(defn webapp-core
  []
  (reagent/create-class
    {:render
     (fn [this]
       [:div
        [components/navbar]
        [(get tab->page (application/get-tab) :div)]])}))

(fw/watch-and-reload
  ;; :websocket-url "ws://localhost:3449/figwheel-ws" default
  :jsload-callback (fn [] (print "reloaded"))) ;; optional callback

(reagent/render-component [webapp-core] (.getElementById js/document "main-area"))
