Mentior is an API client for VTube Studio.

# Install

```shell
$ pip install .
```

# Examples

```python
import asyncio
import mentior

async def main():
    async with mentior.authenticate() as client:
        status = await client.status()
        print(status)

asyncio.run(main())
```
