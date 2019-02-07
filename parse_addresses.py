import json
import os
import binascii

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
database_url = 'postgres://dceraqvcqhmcgu:19271607429d1f3ca9e649f3ea13a61bee4794f7f11ffb622c52a8a74cf87b22@ec2-54-235-68-3.compute-1.amazonaws.com:5432/d4vk8nvjg5nipp'
engine = create_engine(database_url, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
    autoflush=False,
    bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

from sqlalchemy import BIGINT, Column, Integer, String

class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    fully_qualified_name = Column(String)
    company_id = Column(BIGINT)
    wallet_address = Column(String)

    def __repr__(self):
        return '<Account %s> %s' % (str(self.id), self.fully_qualified_name)

company_id = 9

with open('address_list.json') as f:
    addresses = json.loads(f.read())

print(len(addresses))
num_accounts = db_session.query(Account).filter(Account.company_id==company_id).count()
print(num_accounts)

accounts = db_session.query(Account).filter(Account.company_id==company_id)

base_command = 'multichain-cli auditchain %s'

for ind, account in enumerate(accounts):
    wallet_address = addresses[ind]['address']
    label_name = account.fully_qualified_name

    hex_label=binascii.hexlify(label_name.encode('ascii'))
    label_name_hex = hex_label.decode("utf-8")

    print(label_name, '-', wallet_address)
    grant_command = base_command % ('grant "%s" send,receive' % wallet_address)
    #print(grant_command)
    os.system(grant_command)
    publish_from_command = base_command % ('publishfrom "%s" root "%s" %s' % (wallet_address, label_name, label_name_hex))
    #print(publish_from_command)
    os.system(publish_from_command)
    #print()

    account.wallet_address = wallet_address
    db_session.add(account)
    db_session.commit()


