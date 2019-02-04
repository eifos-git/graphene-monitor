Monitor
========
Monitor introduction bla bla 



Add a new Source/Trigger/Action from scratch:
=============================================
Before you create a new Class/Trigger/Action(CTA) check out monitor_variations.factory
for all the implemented CTA's

    1. Create a new CTA that inherits from source.Abstract<CTA> \
       in <CTA>.<CTA>_type
    2. Add the file to __all__ in <CTA>.<CTA>.__init__.py
    3. Add the class to monitor_variations.factory.<CTA>_mappings
    
    




class ABC:
   def __init__(self):
     self._vara 
     self._varb = None

  @property
  def vara(self):
     return self._vara


