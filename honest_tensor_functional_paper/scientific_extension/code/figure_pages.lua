-- Keep each complete figure and its explanatory caption on a dedicated page.
-- This also prevents long-table/float interactions from clipping vector plots.
function Figure(el)
  if FORMAT:match('latex') then
    return {pandoc.RawBlock('latex', '\\clearpage'), el, pandoc.RawBlock('latex', '\\clearpage')}
  end
end
