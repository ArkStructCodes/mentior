Mentior is an asynchronous API client for VTube Studio.

# Install

```shell
$ pip install .
```

# Features

- [x] Getting current VTS statistics
- [x] Getting list of VTS folders
- [x] Getting the currently loaded model
- [x] Getting a list of available VTS models
- [x] Loading a VTS model by its ID
- [x] Moving the currently loaded VTS model
- [x] Requesting list of hotkeys available in current or other VTS model
- [x] Requesting execution of hotkeys
- [ ] Requesting list of expressions and their states
- [ ] Requesting activation/deactivation of expressions
- [ ] Requesting list of ArtMeshes in current model
- [ ] Tint ArtMeshes with color
- [ ] Getting scene lighting overlay color
- [ ] Checking if face is currently found by tracker
- [ ] Requesting list of available tracking parameters
- [ ] Get the value for one specific parameter, default or custom
- [ ] Get the value for all Live2D parameters in the current model
- [ ] Adding new tracking parameters ("custom parameters")
- [ ] Delete custom parameters
- [ ] Feeding in data for default or custom parameters
- [ ] Getting physics settings of currently loaded VTS model
- [ ] Overriding physics settings of currently loaded VTS model
- [ ] Get and/or set NDI settings
- [ ] Requesting list of available items or items in scene
- [ ] Loading item into the scene
- [ ] Removing item from the scene
- [ ] Controling items and item animations
- [ ] Moving items in the scene
- [ ] Asking user to select ArtMeshes
- [ ] Pin items to the model
- [ ] Get list of post-processing effects and state
- [ ] Set post-processing effects

# Examples

```python
import asyncio
import mentior

async def main():
    async with mentior.authenticate() as vts:
        print(await vts.statistics())

asyncio.run(main())
```

You will need to switch to the VTube Studio window to allow the connection.
