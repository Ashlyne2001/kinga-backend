import os

class EnvironmentChecker:
    
    @staticmethod
    def is_env_production():
        """
        Returns true if we are in production and false otherwise
        """
        return os.environ.get("SQL_DATABASE", "") == "kinga_prod" or \
            os.environ.get("DEBUG", 1)
    
    