(ns webapp.core
  (:require [webapp.server :as server]
            [webapp.app :as app]
            [webapp.db.component :as db]
            [webapp.db.schemas :as db-schemas]
            [webapp.db.features :as db-features]
            [webapp.db.datapoints :as db-datapoints]
            [com.stuartsierra.component :as component]))

(defn -main
  [& args]
  (component/start (app/main-system)))
