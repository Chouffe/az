(ns webapp.routes
  (:require [compojure.core :as compojure]
            [webapp.api :as api]
            [compojure.route :as route]
            [org.httpkit.server :as httpkit]))

(compojure/defroutes schema-routes
  (compojure/GET "/" [] (api/schemas-get))
  (compojure/GET "/:schema-id" [schema-id] (api/schema-get schema-id))
  (compojure/POST "/:schema-id" [schema-id & params] "create a schema")
  (compojure/DELETE "/:schema-id" [schema-id] "delete a schema"))

#_(compojure/defroutes feature-routes
  ;; TODO
  )

(compojure/defroutes demo-routes
  (compojure/PUT "/:demo-id" [demo-id] "running demo"))

(compojure/defroutes az-graph-routes
  (compojure/GET "/convergence/:schema-id" [schema-id]
                 "return an az convergence schema-id")
  (compojure/GET "/projection/:schema-id" [schema-id]
                 "return an az projection schema-id")
  (compojure/GET "/feature-importances/:schema-id" [schema-id]
                 "return an az feature-importance schema-id")
  (compojure/GET "/cost-function/:schema-id" [schema-id]
                 "return an az cost function schema-id"))

(compojure/defroutes ab-graph-routes
  (compojure/GET "/convergence/:schema-id" [schema-id]
                 "return an az convergence schema-id")
  (compojure/GET "/cost-function/:schema-id" [schema-id]
                 "return an az cost function schema-id"))

(compojure/defroutes graph-routes
  (compojure/context "/az" az-graph-routes)
  (compojure/context "/ab" ab-graph-routes))

(compojure/defroutes api-routes
  (compojure/GET "/test" [] "SUCCESS")
  (compojure/context "/schemas" [] schema-routes)
  (compojure/context "/demos" [] demo-routes)
  (compojure/context "/graphs" [] graph-routes))

(compojure/defroutes app
  (compojure/context "/api" [] api-routes)
  (compojure/GET "/test/yo" [] "Hello World 2")
  (compojure/GET "/" [] "Hello World")
  (compojure/POST "/" [& params] (do (println params) "POST"))
  (compojure/DELETE "/" [] "DELETE")
  (compojure/PUT "/" [] "PUT")
  #_(compojure/ANY "*" [] "YTYEST")
  )
