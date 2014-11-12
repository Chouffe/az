(ns webapp.demo-data
  (:refer-clojure :exclude [get set]))

(def data
  [{:uuid "demo1"
    :name "Landing Page"
    :schema-id "lp"
    :tests [{:uuid 1
             :title "A/Z testing"
             :type :az
             :tabs [:convergence
                    :projection
                    :cost-function
                    :feature-importances]}
            {:uuid 2
             :title "A/B testing"
             :type :ab
             :tabs [:ab-convergence
                    :ab-cost-function]}]}
   {:uuid "demo2"
    :name "Landing Page with useless features"
    :schema-id "lp2"
    :tests [{:uuid 2
             :title "A/Z testing"
             :type :az
             :tabs [:convergence
                    :projection
                    :cost-function
                    :feature-importances]}
            {:uuid 3
             :title "A/B testing"
             :type :ab
             :tabs [:ab-convergence
                    :ab-cost-function]}]}

   {:uuid "demo3"
    :name "Black Box Optimization"
    :schema-id "blackbox"
    :tests [{:uuid 2
             :title "A/Z testing"
             :type :az
             :tabs [:convergence
                    :projection
                    :cost-function
                    :feature-importances]}]}])

(defn get
  [uuid]
  (first (filter (comp #{uuid} :uuid) data)))

(defn get-test
  [uuid-demo uuid-test]
  (first (filter (comp #{uuid-test} :uuid) (:tests (get uuid-demo)))))
