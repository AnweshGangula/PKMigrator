function Header (header)
  return pandoc.Header(header.level, header.content, pandoc.Attr())
end