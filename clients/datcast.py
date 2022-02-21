from clients.a1_batch import Batch
import json

with open('batches/밴링_라이즈오브킹덤즈', 'r', encoding='utf-8') as f:
    batch2 = Batch(request_batch_json=f.read())
    print(batch2.dict_batch)
batch2.post_request_batch()
batch2.post_crawl_request()
