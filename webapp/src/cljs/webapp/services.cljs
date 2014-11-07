(ns webapp.services
  (:require-macros [cljs.core.async.macros :refer [go]])
  (:require [webapp.state.demo :as demo]
            [webapp.demo-data :as demo-data]
            [webapp.state.schemas :as schemas]
            [cljs-http.client :as http]
            [cljs.core.async :refer [<!]]
            [webapp.utils.ajax :as ajaxu]))

(enable-console-print!)

(defn delete-feature
  [uuid feature-name]
  (schemas/delete-feature uuid feature-name)
  (http/delete (str "http://localhost:5002/api/feature/" uuid)
               {:json-params {:feature_name feature-name}
                :headers {"content-type" "application/json"
                          "accept" "application/json"}}))

(defn add-feature
  [uuid feature-name feature-map]
  (schemas/add-feature uuid feature-name feature-map)
  (go
    (<! (ajaxu/post-json (str "http://localhost:5002/api/feature/" uuid)
                                      {feature-name feature-map} )))
  )

(defn load-demo
  [uuid]
  (print "loading the demo " uuid)
  (demo/set-uuid uuid)
  (print (demo-data/get uuid)))

(defn load-schema
  [uuid]
  (go
    (let [schema (<! (ajaxu/get-json (str "http://localhost:5002/api/schema/" uuid)))]
      (schemas/set schema)))

  ;; TODO: change the state
  ;; API call as well
  )
