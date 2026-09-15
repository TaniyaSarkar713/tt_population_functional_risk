-- Keep each vector figure and caption together, avoiding longtable/float clipping.
function Figure(el)
  if FORMAT:match('latex') then
    return {pandoc.RawBlock('latex', '\\clearpage'), el, pandoc.RawBlock('latex', '\\clearpage')}
  end
end
