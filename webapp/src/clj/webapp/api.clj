(ns webapp.api
  (:require [webapp.db.schemas :as db-schemas]
            [webapp.db.features :as db-features]
            [webapp.db.datapoints :as db-datapoints]
            [webapp.db.abdatapoints :as db-abdatapoints]
            [webapp.utils.data :as datau]
            [clj-http.client :as client]
            [cheshire.core :as cheshire]
            [clojure.string :as string]))

(def jsonify cheshire/generate-string)

;; TODO: DOCUMENTATION

;; -------------------
;;      Schemas
;; -------------------

(defn schema-for-frontend
  [schema]
  (dissoc schema :_id))

(defn schemas-get
  []
  (jsonify {:schemas (mapv schema-for-frontend (db-schemas/get-all))}))

(defn schema-get
  [uuid]
  (->> uuid db-schemas/get-by-uuid schema-for-frontend jsonify))

(defn schema-delete
  [uuid]
  (db-schemas/remove-by-uuid uuid)
  (db-datapoints/delete-by-uuid uuid)
  (jsonify {:error nil}))

(defn schema-create
  [uuid {:keys [features]}]
  (db-schemas/insert uuid features)
  (jsonify {:error nil}))

;; -------------------
;;      Features
;; -------------------

(defn feature-add
  [uuid feature-name {:keys [default distribution params] :as feature-map}]
  {:pre [distribution feature-name]}
  (let [default (if-not (string/blank? default)
                  default
                  0)
        params (if-not params
                 {}
                  params)
        feature-map {(keyword feature-name)
                     {:default default
                      :distribution distribution
                      :params params}}]
    (db-features/add-feature uuid feature-map)
    (jsonify {:error nil})))

(defn feature-remove
  [uuid feature-name]
  (db-features/remove-feature uuid feature-name)
  (jsonify {:error nil}))

;; -------------------
;;      Demos
;; -------------------

(defn demo-run
  [demo-id]
  (when-let [request (future (client/post (str "http://localhost:5004/service/demo/" demo-id)))]
    (jsonify {:demo "running"})))

;; -------------------
;;      Graphs
;; -------------------

(defn graph-projection
  [uuid]
  (when-let [{:keys [features]} (db-schemas/get-by-uuid uuid)]
    (when-let [datapoints (db-datapoints/get-by-uuid uuid)]
      (jsonify
        (datau/datapoints->projection-data datapoints features)))))

(defn graph-convergence
  ([uuid] (graph-convergence uuid false))
  ([uuid ab-testing?]
   (when-let [{:keys [features]} (db-schemas/get-by-uuid uuid)]
     (when-let [datapoints (if ab-testing?
                             (db-abdatapoints/get-by-uuid uuid)
                             (db-datapoints/get-by-uuid uuid))]
       (jsonify
         (datau/datapoints->convergence-data datapoints features))))))

(defn graph-cost-function
  ([uuid] (graph-cost-function uuid false))
  ([uuid ab-testing?]
   (when-let [datapoints (if ab-testing?
                           (db-abdatapoints/get-by-uuid uuid)
                           (db-datapoints/get-by-uuid uuid))]
     (jsonify
       (datau/datapoints->cost-function-data datapoints)))))

(defn graph-feature-importances
  [uuid]
  (client/get (str "http://localhost:5003/service/feature-importances/" uuid)))

;; ----------------
;;     Main
;; ----------------

(defn next-point
  [uuid]
  (when-let [result (client/get (str "http://localhost:5002/api/" uuid))]
    (:body result)))
