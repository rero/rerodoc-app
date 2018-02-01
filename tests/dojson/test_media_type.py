# import pytest
# from conftest import marc2marc, marc2record, record2jsonld, validator

# validator = validator('common/media_type-0.0.1.json')
# assert validator


# # # TODO: suppress
# # def test_jsonld(book_context):
# #     record = {
# #         'recid': '1234',
# #         'media_type': 'http://rdvocab.info/termList/RDAMediaType/1003'
# #     }
# #     converted = record2jsonld(record, book_context)
# #     assert converted == [{
# #         '@id': 'http://doc.rero.ch/record/1234',
# #         'http://rdaregistry.info/Elements/u/mediaType': [{
# #             '@id': 'http://rdvocab.info/termList/RDAMediaType/1003'
# #         }]
# #     }]
