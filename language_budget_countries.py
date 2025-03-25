from mrjob.job import MRJob
from mrjob.step import MRStep

class LanguageBudgetCountries(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer)
        ]

    def mapper(self, _, line):
        # Assuming the input file has fields separated by tabs in the order: title, year, country, budget
        fields = line.split('|')
        if len(fields) != 4:
            return
        
        title, year, country, budget = fields
        try:
            budget = float(budget)
        except ValueError:
            return
        
        if country and budget:
            yield country, (country, budget)

    def reducer(self, language, values):
        countries = set()
        total_budget = 0.0
        
        for country, budget in values:
            countries.add(country)
            total_budget += budget
        
        yield (list(countries), total_budget)

if __name__ == '__main__':
    LanguageBudgetCountries.run()