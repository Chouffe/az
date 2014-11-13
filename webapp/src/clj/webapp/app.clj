(ns webapp.app
  (:require [com.stuartsierra.component :as component]
            webapp.server
            webapp.db.component))


(defn main-system
  []
  (component/system-map
    :database (webapp.db.component/db-component)
    :server (component/using
              (webapp.server/server-component 5000)
              [:database])))
