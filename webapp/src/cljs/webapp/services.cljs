(ns webapp.services
  (:require-macros [cljs.core.async.macros :refer [go]])
  (:require [webapp.state.demo :as demo]
            [webapp.demo-data :as demo-data]
            [webapp.state.schemas :as schemas]
            [webapp.state.experiments :as experiments]
            [webapp.state.convergence :as convergence]
            [webapp.state.next-point :as next-point]
            [webapp.state.ab-convergence :as ab-convergence]
            [webapp.state.cost-function :as cost-function]
            [webapp.state.ab-cost-function :as ab-cost-function]
            [webapp.state.feature-importances :as feature-importances]
            [webapp.state.projection :as projection]
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

(defn create-schema
  [experiment-name feature-map]
  (go
    (<! (ajaxu/post-json (str "http://localhost:5002/api/schema/" experiment-name)
                                      {:features feature-map}))
    (schemas/set {:uuid experiment-name :features feature-map})))

(defn load-schemas
  []
  (go
    (let [{:keys [schemas]} (<! (ajaxu/get-json "http://localhost:5002/api/schemas"))]
      (doseq [schema schemas]
        (schemas/set schema)))))

(defn load-demo
  [uuid]
  (demo/set-uuid uuid))

(defn load-experiment
  [uuid]
  (experiments/set-uuid uuid))

(defn run-demo
  [uuid]
  (go
    (<! (ajaxu/get-json (str "http://localhost:5002/api/demo/" uuid)))))

(defn load-cost-function
  [uuid]
  (go
    (let [{:keys [results]} (<! (ajaxu/get-json (str "http://localhost:5002/api/graph/obj-function/" uuid)))]
      (cost-function/set uuid results))))

(defn load-ab-cost-function
  [uuid]
  (go
    (let [{:keys [results]} (<! (ajaxu/get-json (str "http://localhost:5002/api/ab/graph/obj-function/" uuid)))]
      (ab-cost-function/set uuid results))))

(defn load-feature-importances
  [uuid]
  (go
    (let [data (<! (ajaxu/get-json (str "http://localhost:5002/api/graph/feature-importances/" uuid)))]
      (feature-importances/set uuid data))))

(defn load-convergence
  [uuid]
  (go
    (let [data (<! (ajaxu/get-json (str "http://localhost:5002/api/graph/results/" uuid)))]
      (convergence/set uuid data))))

(defn load-ab-convergence
  [uuid]
  (go
    (let [data (<! (ajaxu/get-json (str "http://localhost:5002/api/ab/graph/results/" uuid)))]
      (ab-convergence/set uuid data))))

(defn load-projection
  [uuid]
  (go
    (let [data (<! (ajaxu/get-json (str "http://localhost:5002/api/graph/obj/" uuid)))]
      (projection/set uuid data))))

(defn load-schema
  [uuid]
  (go
    (let [schema (<! (ajaxu/get-json (str "http://localhost:5002/api/schema/" uuid)))]
      (schemas/set schema))))

(defn get-next-point
  [uuid]
  (go
    (let [point (<! (ajaxu/get-json (str "http://localhost:5002/api/" uuid)))]
      (next-point/set uuid point))))
