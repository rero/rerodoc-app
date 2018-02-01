# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2017 RERO.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, RERO does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""RERO DOC facets configuration."""


document_type = dict(
    terms=dict(
        field="_collections",
        size=1000,
        include='type\.[a-z_]+'
    )
)

udc = dict(
    terms=dict(
        field="_collections",
        size=1000,
        include='udc\.[a-z_]+'
    ),
    aggs=dict(
        sciences_exactes_et_naturelles=dict(
            terms=dict(
                field="_collections",
                size=1000,
                include='udc\.sciences_exactes_et_naturelles\.[a-z_]+'
            ),
            aggs=dict(
                sciences_de_la_terre=dict(
                    terms=dict(
                        field="_collections",
                        size=1000,
                        include='udc\.sciences_exactes_et_naturelles\.sciences_de_la_terre\.[a-z_]+'  # nopep8
                    ),
                    aggs=dict(
                        geologie=dict(
                            terms=dict(
                                field="_collections",
                                size=1000,
                                include='udc\.sciences_exactes_et_naturelles\.sciences_de_la_terre\.geologie\.[a-z_]+'  # nopep8
                            )
                        )
                    )
                )
            )
        )
    )
)

institution = dict(
    terms=dict(
        field="_collections",
        size=1000,
        include='institution\.[a-z_]+'
    ),
    aggs=dict(
        vaud=dict(
            terms=dict(
                field="_collections",
                size=1000,
                include='institution\.vaud\.[a-z_]+'
            )
        ),
        geneve=dict(
            terms=dict(
                field="_collections",
                size=1000,
                include='institution\.geneve\.[a-z_]+'
            )
        ),
        fribourg=dict(
            terms=dict(
                field="_collections",
                size=1000,
                include='institution\.fribourg\.[a-z_]+'
            )
        ),
        neuchatel_jura=dict(
            terms=dict(
                field="_collections",
                size=1000,
                include='institution\.neuchatel_jura\.[a-z_]+'
            )
        ),
        tessin=dict(
            terms=dict(
                field="_collections",
                size=1000,
                include='institution\.tessin\.[a-z_]+'
            )
        ),
    )
)
