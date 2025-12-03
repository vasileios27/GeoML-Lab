
HtmlObject(eckit::Bless& b)
{
}

HtmlObject(eckit::Evolve b)
{
}

static const char* specName()      { return "HtmlObject"; }
static void isa(TypeInfo* t)  { eckit::Isa::add(t,specName()); }
static eckit::Isa* isa()             { return eckit::Isa::get(specName());  }

static void schema(eckit::Schema& s)
{
	s.start(specName(),sizeof(HtmlObject));
	s.end(specName());
}


void describe(std::ostream& s,int depth = 0) const {
	eckit::_startClass(s,depth,specName());
	eckit::_endClass(s,depth,specName());
}



void _export(eckit::Exporter& h) const {
	eckit::_startClass(h,"HtmlObject");
	eckit::_endClass(h,"HtmlObject");
}


