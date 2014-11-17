(ns webapp.routes
  (:require [compojure.core :as compojure]
            [webapp.api :as api]
            [compojure.route :as route]
            [org.httpkit.server :as httpkit]
            webapp.pages.home))

(compojure/defroutes schema-routes
  (compojure/GET "/" [] (api/schemas-get))
  (compojure/GET "/:schema-id" [schema-id] (api/schema-get schema-id))
  (compojure/POST "/:schema-id" [schema-id & params]
                  (api/schema-create schema-id params))
  (compojure/DELETE "/:schema-id" [schema-id]
                    (api/schema-delete schema-id))
  (compojure/context "/features/:schema-id" [schema-id]
    (compojure/POST "/:feature-name" [feature-name & params]
                    (api/feature-add schema-id feature-name params))
    (compojure/DELETE "/:feature-name" [feature-name]
                      (api/feature-remove schema-id feature-name))))

(compojure/defroutes demo-routes
  (compojure/POST "/:demo-id" [demo-id] (api/demo-run demo-id)))

(compojure/defroutes az-graph-routes
  (compojure/GET "/convergence/:schema-id" [schema-id]
                 (api/graph-convergence schema-id))
  (compojure/GET "/projection/:schema-id" [schema-id]
                 (api/graph-projection schema-id))
  (compojure/GET "/feature-importances/:schema-id" [schema-id]
                 (api/graph-feature-importances schema-id))
  (compojure/GET "/cost-function/:schema-id" [schema-id]
                 (api/graph-cost-function schema-id)))

(compojure/defroutes ab-graph-routes
  (compojure/GET "/convergence/:schema-id" [schema-id]
                 (api/graph-convergence schema-id true))
  (compojure/GET "/cost-function/:schema-id" [schema-id]
                 (api/graph-cost-function schema-id true)))

(compojure/defroutes graph-routes
  (compojure/context "/az" [] az-graph-routes)
  (compojure/context "/ab" [] ab-graph-routes))

(compojure/defroutes api-routes
  (compojure/context "/schemas" [] schema-routes)
  (compojure/context "/demos" [] demo-routes)
  (compojure/context "/graphs" [] graph-routes)
  (compojure/GET "/:schema-id" [schema-id] (api/next-point schema-id))
  (compojure/POST "/:schema-id" [schema-id & params] (str "yooo" schema-id "  " params)))

(compojure/defroutes app
  (compojure/context "/api" [] api-routes)
  (compojure/GET "/" [] (webapp.pages.home/home-page))
  (route/resources "/"))
