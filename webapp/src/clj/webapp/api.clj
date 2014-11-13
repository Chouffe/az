(ns webapp.api
  (:require [webapp.db.schemas :as db-schemas]
            [cheshire.core :as cheshire]))

(def jsonify cheshire/generate-string)

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
  (jsonify {:error nil}))

;; -------------------
;;      Features
;; -------------------

(defn feature-add
  [uuid feature-map]
  ;; todo
  nil)

(defn feature-remove
  [uuid feature-name]
  ;; todo
  nil)

;; -------------------
;;      Demos
;; -------------------

;; TODO

;; -------------------
;;      Graphs
;; -------------------

;; TODO

(defn graph-projection
  [uuid]
  ;; todo
  nil)

(defn graph-convergence
  [uuid]
  ;; todo
  nil)

(defn graph-cost-function
  [uuid]
  ;; todo
  nil)

(defn graph-feature-importances
  [uuid]
  ;; todo
  nil)

;; ----------------
;;     Main
;; ----------------

(defn next-point
  [uuid]
  ;; TODO
  nil )

(defn save-point
  [uuid point]
  ;; TODO
  nil)
