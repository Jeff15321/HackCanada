from model import *
from prompt import *

user_role = "Biomass Power Plant Managers"
user_task = "Prepare and manage biomass plant budgets."

model = "gpt-4o-mini"

class BiomassBudgetPipeline(dspy.biomass_budget):
    def __init__(self):
        self.data_collection = data_collection
        self.cost_estimation = cost_estimation
        self.budget_drafting = budget_drafting
        self.stakeholder_communication = stakeholder_communication


    def forward(self, documents, market_data):
        relevant_data = self.data_collection_analysis(documents=documents).relevant_data
        cost_estimates = self.cost_estimation(relevant_data=relevant_data).cost_estimates
        revenue_forecast = self.revenue_forecasting(market_data=market_data).revenue_forecast
        budget_draft = self.budget_drafting(cost_estimates=cost_estimates, revenue_forecast=revenue_forecast).budget_draft

        presentation = self.stakeholder_communication(budget_draft=budget_draft).presentation
        performance_metrics = self.performance_monitoring(budget_draft=budget_draft).performance_metrics
        scenario_report = self.scenario_planning(market_data=market_data).scenario_report

        return {
            "presentation": presentation,
            "performance_metrics": performance_metrics,
            "scenario_report": scenario_report,
        }

if __name__ == "__main__":

    initial_prompt = initialize_initial_task_prompt(user_role, user_task)
    print(initial_prompt)

    print("*"*50)
    print("*"*50)
    print("*"*50)

    resp = run_api(model, initial_prompt)
    print(resp)