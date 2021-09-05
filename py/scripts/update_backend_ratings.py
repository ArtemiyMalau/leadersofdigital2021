from .database import session
from .ranking import methods as rank_methods


if __name__ == '__main__':
	rank_methods.update_backend_ratings(session)