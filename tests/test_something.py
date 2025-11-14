
engine =create_engine(
    "sqlite+pysqlite:///: memory:",
    connect_args={"check_same_thread":False},
    poolclass=staticPool,
)
Testing Session =sessionmaker(bind=engine, expire_on_commit=Flase)
Base.metadata.create_all(bind-engine)
def test_customer_patch
