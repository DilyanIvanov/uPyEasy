# Autogenerated file
def render(info, plugindata):
    yield """
<!- DO NOT CHANGE LINE ABOVE! -->
<TR>
   <TD>Device ID:
   <TD>
      <select name='deviceid'>
      """
    for romcnt in range(0,plugindata["romcnt"]):
        yield """
      <option value='"""
        yield str(plugindata["rom"+str(romcnt)])
        yield """'>"""
        yield str(plugindata["rom"+str(romcnt)])
        yield """</option>
      """
    yield """
      </select>
<TR>
   <TD>Device Resolution:
   <TD>
      <select name='resolution'>
         <option value=9 """
    if plugindata['resolution'] == 9:
        yield """selected"""
    yield """>9</option>
         <option value=10"""
    if plugindata['resolution'] == 10:
        yield """selected"""
    yield """>10</option>
         <option value=11"""
    if plugindata['resolution'] == 11:
        yield """selected"""
    yield """>11</option>
         <option value=12"""
    if plugindata['resolution'] == 12:
        yield """selected"""
    yield """>12</option>
      </select> Bit
"""
    yield str(plugindata['content'])