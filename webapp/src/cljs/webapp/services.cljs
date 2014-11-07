(ns webapp.services
  (:require [webapp.state.demo :as demo]))

(enable-console-print!)

(defn delete-feature
  [uuid feature-name]
  (print "deleting the feature")
  ;; TODO: change the state
  ;; API call as well
  )

(defn add-feature
  [uuid feature-map]
  (print "adding the feature")
  ;; TODO: change the state
  ;; API call as well
  )

(defn load-demo
  [uuid]
  (print "loading the demo " uuid)
  (demo/set-uuid uuid)
  )

(defn load-schema
  [uuid]
  (print "loading the schema " uuid)
  ;; TODO: change the state
  ;; API call as well
  )

(defn load-experiment
  [uuid]
  (print "loading the experiment " uuid)
  )
