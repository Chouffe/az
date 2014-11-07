(ns webapp.routes
  (:require [secretary.core :as secretary :include-macros true :refer [defroute]]
            [goog.events :as events]
            [goog.history.EventType :as EventType]
            [webapp.services :as srv]
            [webapp.state.application :as application])
  (:import goog.History))

(secretary/set-config! :prefix "#")

(defroute home-path "/" []
  (application/set-tab :home))

(defroute demo-path "/demo" []
  (application/set-tab :demo))

(defroute demo-path "/demo/:uuid" [uuid]
  (srv/load-demo uuid)
  (application/set-tab :demo-results))

;; Catch all
(defroute "*" []
  (application/set-tab :home))

;; Quick and dirty history configuration.
(let [h (History.)]
  (goog.events/listen h EventType/NAVIGATE #(secretary/dispatch! (.-token %)))
  (doto h (.setEnabled true)))
