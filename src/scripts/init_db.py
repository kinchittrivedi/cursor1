from sqlalchemy import inspect
from ..app.db import init_engine_and_session
from ..app.models import Base


def main():
	engine = init_engine_and_session()
	Base.metadata.create_all(engine)
	print("DB initialized")


if __name__ == "__main__":
	main()