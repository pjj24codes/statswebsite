from flask import Blueprint, render_template, request, redirect, url_for, abort, flash 
from . import db
from .models import Team, Game, BasketballPlayerStats, SoccerPlayerStats
from datetime import date

leagues = []
statsheetsports = ["basketball", "soccer"]
locate_stats = ["MIAA", "Boys Basketball", 1, "Brockton High School", 1]
continue_data = None
teams = []
players = []


class League:
    def __init__(self, name, acronym, logo):
        self.name = name
        self.acronym = acronym 
        self.logo = logo
        self.sports = []

    def addsport(self, sport_name, divs, teams):
        self.sports.append([sport_name, divs, teams])


leagues.append(League("Massachusetts Interscholastic Athletic Association", "MIAA", "miaa.jpg"))
leagues[0].addsport("Boys Basketball", 5, [["Brockton High School", "Saint John's Preparatory School", "Lowell High School", "Framingham High School", "Lexington High School", "Boston College High School", "Newton North High School", "Brookline High School", "Wachusett Regional High School", "Taunton High School", "Methuen High School", "Shrewsbury High School", "Newton South High School", "Cambridge Rindge & Latin School", "Lawrence High School", "Haverhill High School", "New Bedford High School", "Acton-Boxborough Regional High School", "Needham High School", "Attleboro High School", "Weymouth High School", "Franklin High School", "Andover High School", "Saint John's High School", "Boston Latin School", "Braintree High School", "Revere High School", "Westford Academy", "Durfee High School", "Natick High School", "Lincoln-Sudbury", "Xaverian Brothers High School", "Arlington High School", "Lynn English High School", "Everett High School", "Waltham High School", "Diman Regional Vocational/Technical High School", "Wellesley High School", "Springfield Central High School", "Peabody Veterans Memorial High School", "Barnstable High School", "Malden High School", "Winchester High School", "Chelmsford High School", "Belmont High School", "Concord-Carlisle High School", "Beverly High School", "Quincy High School", "King Philip Regional High School", "North Andover High School", "Bridgewater-Raynham Regional High School", "Plymouth North High School", "Algonquin Regional High School", "Marshfield High School", "Woburn Memorial High School", "Medford High School", "Central Catholic High School", "Bishop Feehan High School", "Catholic Memorial School", "Putnam Vocational/Technical High School", "North High School"],
                                           ["Leominster High School", "Bristol-Plymouth Reg Voc Tech", "North Quincy High School", "Hopkinton High School", "Hingham High School", "Westborough High School", "Bay Path RVT High School", "Reading Memorial High School", "Milford High School", "Sharon High School", "North Attleborough High School", "Chicopee Comprehensive HS", "Somerville High School", "Milton High School", "Oliver Ames High School", "Mansfield High School", "Billerica Memorial High School", "Doherty Memorial High School", "West Springfield High School", "Westfield High School", "Masconomet Reg. High School", "Plymouth South High School", "Silver Lake Reg. High School", "Stoughton High School", "South High Community School", "Walpole High School", "Whitman-Hanson Regional HS", "Dartmouth High School", "Minnechaug Reg. High School", "Norwood Senior High School", "Agawam High School", "Westwood High School", "Duxbury High School", "Somerset Berkley Regional High School", "Marblehead High School", "Fitchburg High School", "Holyoke High School", "Longmeadow High School", "Shepherd Hill Regional HS", "Melrose High School", "Canton High School", "Grafton High School", "Northampton High School", "Nashoba Reg. High School", "Burlington High School", "Scituate High School", "Middleboro High School", "Dracut Senior High School", "Amherst-Pelham Reg High School", "Wayland High School", "Wakefield Memorial High School", "Bedford High School", "Marlborough High School", "Holliston High School", "East Longmeadow High School", "Ashland High School", "Burncoat High School", "Nauset Reg. High School", "Tewksbury Memorial High School", "Danvers High School", "Malden Catholic HS", "Chicopee High School", "Bishop Stang High School", "Archbishop Williams High School", "Pope Francis Preparatory School"],
                                           ["Greater New Bedford RVTHS", "Greater Lowell Tech HS", "Essex North Shore Agric & Tech School", "Southeastern Reg. Voc/Tech School", "Montachusett RVT High School", "Shawsheen Valley Tech School", "Lynn Classical High School", "Whittier RVT High School", "Worcester Technical High School", "Greater Lawrence Tech HS", "Blackstone Valley Reg Voc/Tech HS", "Tantasqua Regional Senior High School", "Boston Latin Academy", "Chelsea High School", "Ludlow High School", "Pembroke High School", "Newburyport High School", "Falmouth High School", "North Middlesex Regional HS", "Foxborough High School", "Medfield High School", "Gloucester High School", "Hanover High School", "Groton-Dunstable Reg. High School", "Auburn High School", "Apponequet Regional H.S.", "Saugus Middle/High School", "Watertown High School", "Wilmington High School", "Dighton-Rehoboth Regional HS", "Dedham High School", "Old Rochester Reg. High School", "Norton High School", "Martha's Vineyard Reg. High Sch.", "Dover-Sherborn High School", "Taconic High School", "Medway High School", "Belchertown High School", "Weston High School", "North Reading High School", "Swampscott High School", "Triton Regional High School", "Norwell High School", "Pentucket Reg. High School", "Nipmuc Regional High School", "Oakmont Regional High School", "Hudson High School", "Springfield HS of Sci. and Tech.", "Fairhaven High School", "Sandwich High School", "Seekonk High School", "Dennis-Yarmouth Regional HS", "Salem High School", "East Bridgewater Jr/Sr High School", "Quabbin Regional High School", "Abington High School", "Bellingham High School", "Stoneham High School", "Lynnfield High School", "Pittsfield High School", "Advanced Math & Science Acad. Charter", "East Boston High School", "Cardinal Spellman High School", "Bishop Fenwick High School", "Saint Mary's High School", "Randolph High School", "Saint Paul Diocesan Jr/Sr HS", "Arlington Catholic High School", "Lowell Catholic High School", "Springfield Int'l Charter School", "Tech Boston Academy", "Charlestown High School"],
                                           ["Northeast Metro. Reg. Voc. School", "O'Bryant High School", "Assabet Valley Reg Tech HS", "Tri-County RVT High School", "Blue Hills Regional Tech Sch.", "Lynn Vocational Technical Inst", "Nashoba Valley Technical High School", "Upper Cape Cod RVT School", "South Shore Voc/Tech. HS", "Madison Park Tech/Voc H.S.", "Winthrop High School", "Joseph Case High School", "South Hadley High School", "Nantucket High School", "Ipswich High School", "Rockland High School", "Northbridge High School", "Excel Academy Charter High School", "Monomoy Regional High School", "Wahconah Regional High School", "Monument Mountain Reg HS", "Bristol County Agricultural HS", "Hamilton-Wenham Reg HS", "Smith Vocational and Agricultural HS", "Millbury Mem.Jr./Sr.H.S.", "High School of Commerce", "Manchester Essex Reg. High School", "Amesbury High School", "Littleton High School", "Lunenburg High School", "Mashpee Middle/High School", "Hampshire Regional Middle/High School", "Gardner High School", "Cohasset High School", "Clinton High School", "Leicester High School", "Tyngsborough High School", "Uxbridge High School", "Sturgis Charter School West", "Sturgis Charter School East", "Southwick Regional School", "Roxbury Prep High School", "West Bridgewater Mid/Sr. HS", "Frontier Regional School", "Oxford High School", "Blackstone-Millville Reg HS", "Carver Middle/High School", "Easthampton High School", "Bourne High School", "KIPP Academy Lynn Collegiate", "Sutton High School", "Ayer Shirley Regional High School", "Matignon High School", "Greenfield High School", "Georgetown Middle/High School", "Millis High School", "Mount Greylock Regional School", "Quaboag Regional Middle/High School", "Bromfield School", "Wareham High School", "David Prouty High School", "Mystic Valley Regional Charter School", "Snowden Int'l School @ Copley", "Cathedral High School", "Saint Joseph Preparatory High School", "Whitinsville Christian School", "Burke High School", "Bishop Connolly High School", "Saint Bernard's High School", "Falmouth Academy", "Maimonides School", "Saint Mary's High School (Westfield)", "Cape Cod Academy", "South Lancaster Academy", "Immaculate Heart of Mary School", "South Shore Christian Academy", "Fellowship Christian Academy"],
                                           ["Minuteman Regional High School", "Keefe Technical HS", "Norfolk County Agricultural", "Pathfinder RVT High School", "Old Colony Reg Voc/Tech HS", "Cape Cod Regional Tech HS", "Franklin County Tech. School", "McCann Technical High School", "Westfield Technical Academy", "Innovation Academy Charter School", "Douglas High School", "Boston Collegiate Charter School", "Westport High School", "Athol High School", "Notre Dame Cristo Rey HS", "Maynard High School", "South Shore Charter Public School", "Hopedale Jr./Sr. High School", "Mahar Regional School", "New Mission High School", "Narragansett Reg. High School", "Tahanto Regional Middle/High School", "Bartlett High School", "Holbrook Middle-High School", "English High School (Boston)", "Rising Tide Charter Public School", "Abby Kelley Foster Reg Charter School", "Boston Prep Charter Public School", "Saint John Paul II High School", "Salem Academy Charter School", "Murdock High School", "Drury High School", "West Boylston Middle/High School", "Southbridge High School", "Excel High School", "Fenway High School", "Lenox Memorial Middle & High School", "Hampden Charter Sch of Science East", "Hull High School", "Ware Jr/Sr High School", "Atlantis Charter School", "Parker Charter Essential School", "Rockport High School", "Renaissance School", "Lee Middle/High School", "Palmer High School", "Edward Kennedy Acad for Health Career", "Neighborhood House Charter School", "Brighton High School", "Prospect Hill Academy Charter School", "Granby Jr./Sr. High School", "Cristo Rey Boston", "Academy of the Pacific Rim", "Dearborn STEM Academy", "Hoosac Valley Middle/High School", "Green Academy", "Avon Mid/High School", "Pioneer Charter School of Science II", "University Park Campus", "John J. Duggan Academy", "Sizer School", "Mount Everett Reg. High School", "Monson High School", "Pioneer Valley Regional School", "Pioneer Charter School of Science", "Community Academy of Sci & Health", "Hopkins Academy", "Gateway Reg. High School", "Turners Falls High School", "Community Charter School of Cambridge", "Baystate Academy Charter Public", "Hampden Charter Schl of Science West", "Pioneer Valley Chinese Immersion Char", "Mohawk Trail Regional HS/MS", "Paulo Freire Social Justice Charter", "Collegiate Charter School of Lowell", "Smith Academy", "North Brookfield Jr./Sr. HS", "Pioneer Valley Christian Academy", "Trivium School", "Libertas Academy Charter School", "Bethany Christian Academy", "Calvary Chapel Academy", "Martha's Vineyard Charter School", "Boston Day and Evening Academy"]])
leagues[0].addsport("Girls Basketball", 5, [["Brockton High School", "Framingham High School", "Lexington High School", "Newton North High School", "Brookline High School", "Wachusett Regional High School", "Taunton High School", "Methuen High School", "Shrewsbury High School", "Newton South High School", "Cambridge Rindge & Latin Schl.", "Lawrence High School", "Haverhill High School", "New Bedford High School", "Acton-Boxborough Reg H.S.", "Needham High School", "Attleboro High School", "Weymouth High School", "Franklin High School", "Andover High School", "Boston Latin School", "Braintree High School", "Revere High School", "Westford Academy", "Durfee High School", "Natick High School", "Lincoln-Sudbury", "Arlington High School", "Lynn English High School", "Everett High School", "Waltham High School", "Diman Regional Voc/Tech HS", "Wellesley High School", "Springfield Central High School", "Peabody Vet. Mem. High School", "Barnstable High School", "Malden High School", "Winchester High School", "Chelmsford High School", "Belmont High School", "Concord-Carlisle High School", "Beverly High School", "Quincy High School", "King Philip Regional H.S.", "North Andover High School", "Bridgewater-Raynham Reg High School", "Plymouth North High School", "Algonquin Reg. High School", "Marshfield High School", "Woburn Memorial High School", "Hopkinton High School", "Medford High School", "Central Catholic High School", "Bishop Feehan High School", "Malden Catholic HS"],
                                            ["Lowell High School", "Leominster High School", "Bristol-Plymouth Reg Voc Tech", "North Quincy High School", "Hingham High School", "Westborough High School", "Bay Path RVT High School", "Reading Memorial High School", "Milford High School", "Sharon High School", "North Attleborough High School", "Chicopee Comprehensive HS", "Somerville High School", "Milton High School", "Oliver Ames High School", "Mansfield High School", "Billerica Memorial High School", "Doherty Memorial High School", "West Springfield High School", "Westfield High School", "Masconomet Reg. High School", "Plymouth South High School", "Silver Lake Reg. High School", "Stoughton High School", "South High Community School", "Walpole High School", "Whitman-Hanson Regional HS", "Dartmouth High School", "Minnechaug Reg. High School", "Norwood Senior High School", "Agawam High School", "Westwood High School", "Duxbury High School", "Somerset Berkley Regional High School", "Marblehead High School", "Fitchburg High School", "Holyoke High School", "Longmeadow High School", "Shepherd Hill Regional HS", "Melrose High School", "Canton High School", "Grafton High School", "Northampton High School", "Nashoba Reg. High School", "Burlington High School", "Scituate High School", "Middleboro High School", "Dracut Senior High School", "Amherst-Pelham Reg High School", "Wayland High School", "Wakefield Memorial High School", "Bedford High School", "Marlborough High School", "Holliston High School", "East Longmeadow High School", "Ashland High School", "Nauset Reg. High School", "Tewksbury Memorial High School", "Danvers High School", "Pembroke High School", "Medfield High School", "Chicopee High School", "Notre Dame Academy (H)", "Bishop Stang High School", "Ursuline Academy", "Archbishop Williams High School", "Cardinal Spellman High School", "Bishop Fenwick High School"],
                                            ["Greater New Bedford RVTHS", "Greater Lowell Tech HS", "Essex North Shore Agric & Tech School", "Southeastern Reg. Voc/Tech School", "Montachusett RVT High School", "Shawsheen Valley Tech School", "Lynn Classical High School", "Whittier RVT High School", "Worcester Technical High School", "Blackstone Valley Reg Voc/Tech HS", "Tantasqua Regional Senior High School", "Boston Latin Academy", "Putnam Voc/Tech High School", "Chelsea High School", "Ludlow High School", "Burncoat High School", "Newburyport High School", "Falmouth High School", "North Middlesex Regional HS", "Foxborough High School", "Gloucester High School", "Hanover High School", "Groton-Dunstable Reg. High School", "Auburn High School", "Apponequet Regional H.S.", "Saugus Middle/High School", "Watertown High School", "Wilmington High School", "Dighton-Rehoboth Regional HS", "Dedham High School", "Old Rochester Reg. High School", "North High School", "Norton High School", "Martha's Vineyard Reg. High Sch.", "Dover-Sherborn High School", "Taconic High School", "Medway High School", "Belchertown High School", "Weston High School", "North Reading High School", "Swampscott High School", "Triton Regional High School", "Norwell High School", "Pentucket Reg. High School", "Nipmuc Regional High School", "Oakmont Regional High School", "Hudson High School", "Fairhaven High School", "Sandwich High School", "Seekonk High School", "Dennis-Yarmouth Regional HS", "Salem High School", "East Bridgewater Jr/Sr High School", "Quabbin Regional High School", "Abington High School", "Bellingham High School", "Stoneham High School", "Lynnfield High School", "Pittsfield High School", "Advanced Math & Science Acad. Charter", "Ipswich High School", "Saint Mary's High School", "Fontbonne Academy", "Saint Paul Diocesan Jr/Sr HS", "Pope Francis Preparatory School", "Arlington Catholic High School", "Lowell Catholic High School", "Notre Dame Academy (W)", "Springfield Int'l Charter School"],
                                            ["Greater Lawrence Tech HS", "Northeast Metro. Reg. Voc. School", "O'Bryant High School", "Assabet Valley Reg Tech HS", "Tri-County RVT High School", "Blue Hills Regional Tech Sch.", "Lynn Vocational Technical Inst", "Nashoba Valley Technical High School", "Upper Cape Cod RVT School", "South Shore Voc/Tech. HS", "Springfield HS of Sci. and Tech.", "Madison Park Tech/Voc H.S.", "Winthrop High School", "East Boston High School", "Joseph Case High School", "South Hadley High School", "Nantucket High School", "Rockland High School", "Northbridge High School", "Excel Academy Charter High School", "Monomoy Regional High School", "Wahconah Regional High School", "Monument Mountain Reg HS", "Bristol County Agricultural HS", "Hamilton-Wenham Reg HS", "Smith Vocational and Agricultural HS", "Millbury Mem.Jr./Sr.H.S.", "High School of Commerce", "Manchester Essex Reg. High School", "Randolph High School", "Amesbury High School", "Littleton High School", "Lunenburg High School", "Mashpee Middle/High School", "Hampshire Regional Middle/High School", "Gardner High School", "Cohasset High School", "Clinton High School", "Leicester High School", "Tyngsborough High School", "Uxbridge High School", "Sturgis Charter School West", "Sturgis Charter School East", "Southwick Regional School", "Roxbury Prep High School", "West Bridgewater Mid/Sr. HS", "Frontier Regional School", "Oxford High School", "Blackstone-Millville Reg HS", "Carver Middle/High School", "Easthampton High School", "Bourne High School", "KIPP Academy Lynn Collegiate", "Sutton High School", "Ayer Shirley Regional High School", "Matignon High School", "Georgetown Middle/High School", "Millis High School", "Mount Greylock Regional School", "Quaboag Regional Middle/High School", "Bromfield School", "Wareham High School", "David Prouty High School", "Mystic Valley Regional Charter School", "Cathedral High School", "Mount Alvernia High School", "Saint Joseph Preparatory High School", "Whitinsville Christian School", "Bishop Connolly High School", "Saint Bernard's High School", "Falmouth Academy", "Maimonides School", "Academy of Notre Dame", "Saint Mary's High School (Westfield)", "Cape Cod Academy", "South Lancaster Academy", "Immaculate Heart of Mary School", "South Shore Christian Academy", "Fellowship Christian Academy", "Bethany Christian Academy"],
                                            ["Minuteman Regional High School", "Norfolk County Agricultural", "Pathfinder RVT High School", "Old Colony Reg Voc/Tech HS", "Cape Cod Regional Tech HS", "Franklin County Tech. School", "McCann Technical High School", "Westfield Technical Academy", "Innovation Academy Charter School", "Douglas High School", "Greenfield High School", "Tech Boston Academy", "Boston Collegiate Charter School", "Westport High School", "Snowden Int'l School @ Copley", "Athol High School", "Notre Dame Cristo Rey HS", "Maynard High School", "South Shore Charter Public School", "Hopedale Jr./Sr. High School", "Mahar Regional School", "Charlestown High School", "New Mission High School", "Narragansett Reg. High School", "Tahanto Regional Middle/High School", "Bartlett High School", "Holbrook Middle-High School", "English High School (Boston)", "Rising Tide Charter Public School", "Abby Kelley Foster Reg Charter School", "Boston Prep Charter Public School", "Saint John Paul II High School", "Salem Academy Charter School", "Murdock High School", "Drury High School", "West Boylston Middle/High School", "Southbridge High School", "Excel High School", "Fenway High School", "Lenox Memorial Middle & High School", "Hampden Charter Sch of Science East", "Hull High School", "Ware Jr/Sr High School", "Atlantis Charter School", "Parker Charter Essential School", "Rockport High School", "Renaissance School", "Lee Middle/High School", "Palmer High School", "Edward Kennedy Acad for Health Career", "Neighborhood House Charter School", "Brighton High School", "Prospect Hill Academy Charter School", "Granby Jr./Sr. High School", "Cristo Rey Boston", "Academy of the Pacific Rim", "Hoosac Valley Middle/High School", "Green Academy", "Avon Mid/High School", "Pioneer Charter School of Science II", "University Park Campus", "John J. Duggan Academy", "Sizer School", "Burke High School", "Mount Everett Reg. High School", "Monson High School", "Pioneer Valley Regional School", "Pioneer Charter School of Science", "Community Academy of Sci & Health", "Hopkins Academy", "Gateway Reg. High School", "Turners Falls High School", "Community Charter School of Cambridge", "Quincy Upper School", "Hampden Charter Schl of Science West", "Pioneer Valley Chinese Immersion Char", "Mohawk Trail Regional HS/MS", "Baystate Academy Charter Public", "Collegiate Charter School of Lowell", "Smith Academy", "North Brookfield Jr./Sr. HS", "Pioneer Valley Christian Academy", "Trivium School", "Libertas Academy Charter School", "Martha's Vineyard Charter School", "Boston Day and Evening Academy"]])
leagues[0].addsport("Boys Soccer", 5, [["Brockton High School", "Saint John's Preparatory School", "Lowell High School", "Framingham High School", "Lexington High School", "Boston College High School", "Newton North High School", "Brookline High School", "Wachusett Regional High School", "Taunton High School", "Methuen High School", "Shrewsbury High School", "Newton South High School", "Cambridge Rindge & Latin Schl.", "Lawrence High School", "Haverhill High School", "New Bedford High School", "Acton-Boxborough Reg H.S.", "Needham High School", "Leominster High School", "Attleboro High School", "Weymouth High School", "Franklin High School", "Andover High School", "Saint John's High School", "Boston Latin School", "Braintree High School", "Westford Academy", "Durfee High School", "Natick High School", "Lincoln-Sudbury Reg. High School", "Xaverian Brothers High School", "Arlington High School", "Lynn English High School", "Everett High School", "Waltham High School", "Diman Regional Voc/Tech HS", "Wellesley High School", "Springfield Central High School", "Peabody Vet. Mem. High School", "Barnstable High School", "Malden High School", "Winchester High School", "Chelmsford High School", "Belmont High School", "Concord-Carlisle High School", "Beverly High School", "King Philip Regional H.S.", "North Andover High School", "Bridgewater-Raynham Reg High School", "Plymouth North High School", "Algonquin Reg. High School", "Marshfield High School", "Medford High School", "Central Catholic High School", "Bishop Feehan High School", "Somerville High School", "Catholic Memorial School", "Ludlow High School"],
                                       ["Revere High School", "Southeastern Reg. Voc/Tech School", "Bristol-Plymouth Reg Voc Tech", "Lynn Classical High School", "North Quincy High School", "Quincy High School", "North High School", "Woburn Memorial High School", "Hopkinton High School", "Hingham High School", "Westborough High School", "Reading Memorial High School", "Milford High School", "Sharon High School", "North Attleborough High School", "Chicopee Comprehensive HS", "Milton High School", "Oliver Ames High School", "Mansfield High School", "Billerica Memorial High School", "Doherty Memorial High School", "West Springfield High School", "Westfield High School", "Masconomet Reg. High School", "Plymouth South High School", "Silver Lake Reg. High School", "Stoughton High School", "South High Community School", "Walpole High School", "Whitman-Hanson Regional HS", "Dartmouth High School", "Minnechaug Reg. High School", "Norwood Senior High School", "Agawam High School", "Westwood High School", "Duxbury High School", "Somerset Berkley Regional High School", "Putnam Voc/Tech High School", "Marblehead High School", "Fitchburg High School", "Longmeadow High School", "Shepherd Hill Regional HS", "Melrose High School", "Canton High School", "Grafton High School", "Northampton High School", "Nashoba Reg. High School", "Burlington High School", "Chelsea High School", "Scituate High School", "Middleboro High School", "Dracut Senior High School", "Amherst-Pelham Reg High School", "Wayland High School", "Wakefield Memorial High School", "Bedford High School", "Marlborough High School", "East Longmeadow High School", "Malden Catholic HS"],
                                       ["Greater New Bedford RVTHS", "Greater Lowell Tech HS", "Essex North Shore Agric & Tech School", "Montachusett RVT High School", "Shawsheen Valley Tech School", "Whittier RVT High School", "Blackstone Valley Reg Voc/Tech HS", "Tantasqua Regional Senior High School", "Boston Latin Academy", "Assabet Valley Reg Tech HS", "Holyoke High School", "Holliston High School", "Burncoat High School", "Ashland High School", "Nauset Reg. High School", "Tewksbury Memorial High School", "Danvers High School", "Pembroke High School", "Newburyport High School", "Falmouth High School", "North Middlesex Regional HS", "Foxborough High School", "Medfield High School", "Gloucester High School", "Chicopee High School", "Hanover High School", "Groton-Dunstable Reg. High School", "Auburn High School", "Apponequet Regional H.S.", "Saugus Middle/High School", "Watertown High School", "Wilmington High School", "Dighton-Rehoboth Regional HS", "Dedham High School", "Old Rochester Reg. High School", "Norton High School", "Martha's Vineyard Reg. High Sch.", "Dover-Sherborn High School", "Taconic High School", "Medway High School", "Belchertown High School", "Weston High School", "North Reading High School", "Swampscott High School", "Triton Regional High School", "Norwell High School", "Pentucket Reg. High School", "Nipmuc Regional High School", "Oakmont Regional High School", "Springfield HS of Sci. and Tech.", "Hudson High School", "Fairhaven High School", "Sandwich High School", "Norfolk County Agricultural", "Seekonk High School", "Dennis-Yarmouth Regional HS", "Salem High School", "East Bridgewater Jr/Sr High School", "Bishop Stang High School", "Archbishop Williams High School", "Cardinal Spellman High School", "Bishop Fenwick High School", "Saint Mary's High School", "Pope Francis Preparatory School", "Arlington Catholic High School"],
                                       ["Greater Lawrence Tech HS", "Bay Path RVT High School", "Northeast Metro. Reg. Voc. School", "O'Bryant High School", "Tri-County RVT High School", "Blue Hills Regional Tech Sch.", "Lynn Vocational Technical Inst", "South Shore Voc/Tech. HS", "Minuteman Regional High School", "Madison Park Tech/Voc H.S.", "Quabbin Regional High School", "Abington High School", "Bellingham High School", "Stoneham High School", "Lynnfield High School", "Pittsfield High School", "Advanced Math & Science Acad. Charter", "Winthrop High School", "East Boston High School", "Joseph Case High School", "South Hadley High School", "Nantucket High School", "Ipswich High School", "Rockland High School", "Northbridge High School", "Excel Academy Charter High School", "Monomoy Regional High School", "Wahconah Regional High School", "Monument Mountain Reg HS", "Hamilton-Wenham Reg HS", "Millbury Mem.Jr./Sr.H.S.", "Westfield Technical Academy", "High School of Commerce", "Manchester Essex Reg. High School", "Randolph High School", "Amesbury High School", "Littleton High School", "Lunenburg High School", "Mashpee Middle/High School", "Hampshire Regional Middle/High School", "Gardner High School", "Cohasset High School", "Clinton High School", "Saint Paul Diocesan Jr/Sr HS", "Leicester High School", "Uxbridge High School", "Tyngsborough High School", "Sturgis Charter School West", "Sturgis Charter School East", "Southwick Regional School", "West Bridgewater Mid/Sr. HS", "Frontier Regional School", "Lowell Catholic High School", "Oxford High School", "Bartlett High School", "Easthampton High School", "Bourne High School", "Cristo Rey Boston", "Whitinsville Christian School", "Bishop Connolly High School", "Falmouth Academy", "Maimonides School", "Cape Cod Academy", "South Lancaster Academy", "South Shore Christian Academy", "Trivium School", "Fellowship Christian Academy", "Trinity Christian Academy"],
                                       ["Nashoba Valley Technical High School", "Upper Cape Cod RVT School", "Keefe Technical HS", "Pathfinder RVT High School", "Old Colony Reg Voc/Tech HS", "Cape Cod Regional Tech HS", "Franklin County Tech. School", "McCann Technical High School", "Bristol County Agricultural HS", "Smith Vocational and Agricultural HS", "Roxbury Prep High School", "Snowden Int'l School @ Copley", "Innovation Academy Charter School", "KIPP Academy Lynn Collegiate", "Sutton High School", "Ayer Shirley Regional High School", "Matignon High School", "Douglas High School", "Greenfield High School", "Georgetown Middle/High School", "Millis High School", "Quaboag Regional Middle/High School", "Mount Greylock Regional School", "Bromfield School", "Wareham High School", "David Prouty High School", "Mystic Valley Regional Charter School", "Springfield Int'l Charter School", "Tech Boston Academy", "Boston Collegiate Charter School", "Westport High School", "Athol High School", "Maynard High School", "Hopedale Jr./Sr. High School", "Mahar Regional School", "Charlestown High School", "New Mission High School", "Narragansett Reg. High School", "Tahanto Regional Middle/High School", "Holbrook Middle-High School", "Rising Tide Charter Public School", "Abby Kelley Foster Reg Charter School", "Excel High School", "Saint John Paul II High School", "Salem Academy Charter School", "Drury High School", "West Boylston Middle/High School", "Lenox Memorial Middle & High School", "Hampden Charter Sch of Science East", "Ware Jr/Sr High School", "Hull High School", "Atlantis Charter School", "Parker Charter Essential School", "Rockport High School", "Renaissance School", "Brighton High School", "Neighborhood House Charter School", "Prospect Hill Academy Charter School", "Granby Jr./Sr. High School", "Saint Joseph Preparatory High School", "Burke High School", "Hoosac Valley Middle/High School", "Avon Mid/High School", "University Park Campus", "John J. Duggan Academy", "Sizer School", "Mount Everett Reg. High School", "Monson High School", "Boston International High School", "Pioneer Valley Regional School", "Pioneer Charter School of Science", "Community Academy of Sci & Health", "Hopkins Academy", "Gateway Reg. High School", "Community Charter School of Cambridge", "Pioneer Valley Chinese Immersion Char", "Mohawk Trail Regional HS/MS", "Collegiate Charter School of Lowell", "Smith Academy", "Saint Mary's High School (Westfield)", "North Brookfield Jr./Sr. HS", "Pioneer Valley Christian Academy", "Libertas Academy Charter School"]])
leagues[0].addsport("Girls Soccer", 5, [['Brockton High School', 'Framingham High School', 'Lexington High School', 'Newton North High School', 'Brookline High School', 'Wachusett Regional High School', 'Taunton High School', 'Methuen High School', 'Shrewsbury High School', 'Newton South High School', 'Cambridge Rindge & Latin Schl.', 'Lawrence High School', 'Haverhill High School', 'New Bedford High School', 'Acton-Boxborough Reg H.S.', 'Needham High School', 'Attleboro High School', 'Weymouth High School', 'Franklin High School', 'Andover High School', 'Boston Latin School', 'Braintree High School', 'Westford Academy', 'Durfee High School', 'Natick High School', 'Lincoln-Sudbury Reg. High School', 'Arlington High School', 'Lynn English High School', 'Everett High School', 'Waltham High School', 'Diman Regional Voc/Tech HS', 'Wellesley High School', 'Springfield Central High School', 'Peabody Vet. Mem. High School', 'Barnstable High School', 'Winchester High School', 'Chelmsford High School', 'Belmont High School', 'Concord-Carlisle High School', 'Beverly High School', 'King Philip Regional H.S.', 'North Andover High School', 'Bridgewater-Raynham Reg High School', 'Plymouth North High School', 'Algonquin Reg. High School', 'Marshfield High School', 'Woburn Memorial High School', 'Hopkinton High School', 'Medford High School', 'Central Catholic High School', 'Bishop Feehan High School'],
                                        ['Lowell High School', 'Leominster High School', 'Southeastern Reg. Voc/Tech School', 'Malden High School', 'Bristol-Plymouth Reg Voc Tech', 'Lynn Classical High School', 'North Quincy High School', 'Quincy High School', 'Hingham High School', 'Westborough High School', 'Reading Memorial High School', 'Milford High School', 'Sharon High School', 'North Attleborough High School', 'Chicopee Comprehensive HS', 'Somerville High School', 'Milton High School', 'Oliver Ames High School', 'Mansfield High School', 'Billerica Memorial High School', 'Doherty Memorial High School', 'West Springfield High School', 'Westfield High School', 'Masconomet Reg. High School', 'Plymouth South High School', 'Silver Lake Reg. High School', 'Stoughton High School', 'Walpole High School', 'Whitman-Hanson Regional HS', 'Dartmouth High School', 'Minnechaug Reg. High School', 'Norwood Senior High School', 'Agawam High School', 'Westwood High School', 'Duxbury High School', 'Somerset Berkley Regional High School', 'Putnam Voc/Tech High School', 'Marblehead High School', 'Fitchburg High School', 'Longmeadow High School', 'Shepherd Hill Regional HS', 'Melrose High School', 'Canton High School', 'Grafton High School', 'Northampton High School', 'Nashoba Reg. High School', 'Burlington High School', 'Chelsea High School', 'Scituate High School', 'Middleboro High School', 'Dracut Senior High School', 'Amherst-Pelham Reg High School', 'Wayland High School', 'Wakefield Memorial High School', 'Bedford High School', 'Ludlow High School', 'Marlborough High School', 'Holliston High School', 'East Longmeadow High School', 'Ashland High School', 'Burncoat High School', 'Malden Catholic HS', 'Notre Dame Academy (H)', "Bishop Stang High School"],
                                        ['Greater New Bedford RVTHS', 'Greater Lowell Tech HS', 'Essex North Shore Agric & Tech School', 'Revere High School', 'Montachusett RVT High School', 'Shawsheen Valley Tech School', 'Whittier RVT High School', 'Worcester Technical High School', 'Blackstone Valley Reg Voc/Tech HS', 'Tantasqua Regional Senior High School', 'Boston Latin Academy', 'Assabet Valley Reg Tech HS', 'Holyoke High School', 'Nauset Reg. High School', 'Tewksbury Memorial High School', 'Danvers High School', 'Pembroke High School', 'Newburyport High School', 'Falmouth High School', 'North Middlesex Regional HS', 'Foxborough High School', 'Medfield High School', 'Gloucester High School', 'Chicopee High School', 'Hanover High School', 'Groton-Dunstable Reg. High School', 'Auburn High School', 'Apponequet Regional H.S.', 'Saugus Middle/High School', 'Watertown High School', 'Wilmington High School', 'Dighton-Rehoboth Regional HS', 'Dedham High School', 'Old Rochester Reg. High School', 'Norton High School', "Martha's Vineyard Reg. High Sch.", 'Dover-Sherborn High School', 'Taconic High School', 'Medway High School', 'Belchertown High School', 'Weston High School', 'North Reading High School', 'Swampscott High School', 'Triton Regional High School', 'Norwell High School', 'Pentucket Reg. High School', 'Nipmuc Regional High School', 'Oakmont Regional High School', 'Hudson High School', 'Fairhaven High School', 'Sandwich High School', 'Norfolk County Agricultural', 'Seekonk High School', 'Dennis-Yarmouth Regional HS', 'Salem High School', 'East Bridgewater Jr/Sr High School', 'Quabbin Regional High School', 'Stoneham High School', 'Ursuline Academy', 'Archbishop Williams High School', 'Cardinal Spellman High School', 'Bishop Fenwick High School', "Saint Mary's High School", 'Fontbonne Academy', 'Pope Francis Preparatory School', 'Arlington Catholic High School', 'Notre Dame Academy (W)'],
                                        ['Greater Lawrence Tech HS', 'Bay Path RVT High School', 'Northeast Metro. Reg. Voc. School', 'O\'Bryant High School', 'South High Community School', 'Tri-County RVT High School', 'Blue Hills Regional Tech Sch.', 'Lynn Vocational Technical Inst', 'South Shore Voc/Tech. HS', 'Minuteman Regional High School', 'Madison Park Tech/Voc H.S.', 'Abington High School', 'Bellingham High School', 'Lynnfield High School', 'Pittsfield High School', 'Advanced Math & Science Acad. Charter', 'Winthrop High School', 'East Boston High School', 'Joseph Case High School', 'South Hadley High School', 'Nantucket High School', 'Ipswich High School', 'Rockland High School', 'Northbridge High School', 'Excel Academy Charter High School', 'Monomoy Regional High School', 'Wahconah Regional High School', 'Monument Mountain Reg HS', 'Hamilton-Wenham Reg HS', 'Millbury Mem.Jr./Sr.H.S.', 'Westfield Technical Academy', 'High School of Commerce', 'Manchester Essex Reg. High School', 'Randolph High School', 'Amesbury High School', 'Littleton High School', 'Lunenburg High School', 'Mashpee Middle/High School', 'Hampshire Regional Middle/High School', 'Gardner High School', 'Cohasset High School', 'Clinton High School', 'Saint Paul Diocesan Jr/Sr HS', 'Leicester High School', 'Tyngsborough High School', 'Uxbridge High School', 'Sturgis Charter School West', 'Sturgis Charter School East', 'Southwick Regional School', 'West Bridgewater Mid/Sr. HS', 'Frontier Regional School', 'Lowell Catholic High School', 'Oxford High School', 'Blackstone-Millville Reg HS', 'Carver Middle/High School', 'Easthampton High School', 'Bourne High School', 'Sutton High School', 'Cathedral High School', 'Mount Alvernia High School', 'Bishop Connolly High School', 'Saint Bernard\'s High School', 'Falmouth Academy', 'Maimonides School', 'Cape Cod Academy', 'South Shore Christian Academy', 'Trivium School'],
                                        ['Nashoba Valley Technical High School', 'Upper Cape Cod RVT School', 'Pathfinder RVT High School', 'Old Colony Reg Voc/Tech HS', 'Cape Cod Regional Tech HS', 'Franklin County Tech. School', 'McCann Technical High School', 'Bristol County Agricultural HS', 'Smith Vocational and Agricultural HS', 'Roxbury Prep High School', 'Snowden Int\'l School @ Copley', 'Innovation Academy Charter School', 'KIPP Academy Lynn Collegiate', 'Ayer Shirley Regional High School', 'Matignon High School', 'Douglas High School', 'Greenfield High School', 'Georgetown Middle/High School', 'Millis High School', 'Mount Greylock Regional School', 'Quaboag Regional Middle/High School', 'Bromfield School', 'Wareham High School', 'David Prouty High School', 'Mystic Valley Regional Charter School', 'Springfield Int\'l Charter School', 'Tech Boston Academy', 'Boston Collegiate Charter School', 'Westport High School', 'Athol High School', 'Maynard High School', 'Hopedale Jr./Sr. High School', 'Mahar Regional School', 'Charlestown High School', 'New Mission High School', 'Narragansett Reg. High School', 'Tahanto Regional Middle/High School', 'Bartlett High School', 'Holbrook Middle-High School', 'Rising Tide Charter Public School', 'Abby Kelley Foster Reg Charter School', 'Excel High School', 'Saint John Paul II High School', 'Salem Academy Charter School', 'Drury High School', 'West Boylston Middle/High School', 'Lenox Memorial Middle & High School', 'Hampden Charter Sch of Science East', 'Hull High School', 'Ware Jr/Sr High School', 'Atlantis Charter School', 'Parker Charter Essential School', 'Rockport High School', 'Renaissance School', 'Lee Middle/High School', 'Palmer High School', 'Neighborhood House Charter School', 'Brighton High School', 'Prospect Hill Academy Charter School', 'Granby Jr./Sr. High School', 'Saint Joseph Preparatory High School', 'Whitinsville Christian School', 'Burke High School', 'Hoosac Valley Middle/High School', 'Avon Mid/High School', 'Pioneer Charter School of Science II', 'University Park Campus', 'John J. Duggan Academy', 'Sizer School', 'Mount Everett Reg. High School', 'Monson High School', 'Boston International High School', 'Pioneer Valley Regional School', 'Pioneer Charter School of Science', 'Hopkins Academy', 'Gateway Reg. High School', 'Community Charter School of Cambridge', 'Pioneer Valley Chinese Immersion Char', 'Mohawk Trail Regional HS/MS', 'Collegiate Charter School of Lowell', 'Academy of Notre Dame ', 'Smith Academy', 'Saint Mary\'s High School (Westfield)', 'North Brookfield Jr./Sr. HS', 'Libertas Academy Charter School']])

leagues.append(League("Massachusetts Charter School Athletic Organization", "MCSAO", "mcsao.jpg"))
leagues[1].addsport("Boys Basketball", 4, [["Community Charter", "Excel Academy", "Pioneer", "Pioneer II", "Prospect Hill", "Salem Academy"],
                                           ["Boston Collegiate", "Brooke High School", "Edward M. Kennedy", "Neighborhood House", "Roxbury Prep"],
                                           ["Academy of the Pacific Rim", "Boston Prep", "Foxborough Regional", "South Shore"],
                                           ["City on A Hill", "Codman Academy", "MATCH", "New Heights", "Argosy Collegiate", "Collegiate Lowell"]])
leagues[1].addsport("Girls Basketball", 4, [["Community Charter", "Excel Academy", "Pioneer", "Pioneer II", "Prospect Hill", "Salem Academy"],
                                           ["Boston Collegiate", "Brooke High School", "Edward M. Kennedy", "Neighborhood House", "Roxbury Prep"],
                                           ["Academy of the Pacific Rim", "Boston Prep", "Foxborough Regional", "South Shore"],
                                           ["Codman Academy", "MATCH", "New Heights", "Argosy Collegiate", "Collegiate Lowell"]])
leagues[1].addsport("Boys Soccer", 4, [["Excel", "Pioneer", "CCSC", "Prospect Hill", "Salem Academy"],
                                        ["Boston Collegiate", "Brooke High School", "Neighborhood House", "Roxbury Prep"],
                                        ["Academy of the Pacific Rim", "Boston Prep", "Foxborough Regional", "South Shore"],
                                        ["City on A Hill", "Codman Academy", "Phoenix", "New Heights", "Argosy Collegiate", "Collegiate Lowell", "Libertas Academy"]])
leagues[1].addsport("Girls Soccer", 4, [["Excel", "Pioneer", "Prospect Hill", "Salem Academy"],
                                        ["Boston Collegiate", "Brooke High School", "Neighborhood House", "Roxbury Prep"],
                                        ["Academy of the Pacific Rim", "Boston Prep", "Foxborough Regional", "South Shore"],
                                        ["Codman Academy", "Phoenix", "New Heights", "Argosy Collegiate", "Collegiate Lowell", "Libertas Academy"]])
for league in range(0, len(leagues)):
    for sport in range(0, len(leagues[league].sports)):
        for div in range(0, len(leagues[league].sports[sport][2])):
            leagues[league].sports[sport][2][div] = sorted(leagues[league].sports[sport][2][div])
            for team in leagues[league].sports[sport][2][div]:
                if teams.count(team) == 0:
                    teams.append(team)
teams = sorted(teams)


views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def home():
    # Adds teams to database
    # add_teams = []
    # for league in leagues:
    #     for sport in league.sports:
    #         for div in range(0, sport[1]):
    #             for team in sport[2][div]:
    #                 league_sport_division_team = league.acronym + " " + sport[0] + " " + str(div+1) + " " + team
    #                 existing_team = Team.query.filter_by(league_sport_division_team=league_sport_division_team).first()
    #                 if not existing_team:
    #                     add_team = Team(league_sport_division_team=league_sport_division_team, league=league.acronym, sport=sport[0], division=(div+1), team=team, wins=0, losses=0, draws=0)
    #                     add_teams.append(add_team)
    # db.session.add_all(add_teams)
    # db.session.commit()
    return render_template("home.html")


@views.route("/statssheets", methods=["GET", "POST"])
def statssheets():
    global continue_data
    global players
    if request.method == "POST":
        continue_data = None
        players = []
        if "basketball_sheet" in request.form:
            return redirect(url_for("views.basketballstatssheets"))
        elif "soccer_sheet" in request.form:
            return redirect(url_for("views.soccerstatssheets"))
    return render_template("statssheets.html")

@views.route("/basketballstatssheets", methods=["GET", "POST"])
def basketballstatssheets():
    global continue_data
    global players
    if request.method == "POST":
        if "add_player" in request.form:
            new_player_name = request.form.get('playername')
            new_player_number = request.form.get('playernumber')
            if not new_player_name:
                flash("Please add a name to the player", category="error")
            elif not new_player_number:
                flash("Please add a number to the player", category="error")
            else:
                players.append({"Number": new_player_number, "Name": new_player_name, "FG": 0, "FGA": 0, "FG%": "0.0%", "3P": 0, "3PA": 0, "3P%": "0.0%", "FT": 0, "FTA": 0, "FT%": "0.0%", "TRB": 0, "AST": 0, "PTS": 0})
        elif "add1" in request.form:
            add_one_placement = request.form.get('add1').split(", ")
            players[int(add_one_placement[0])][add_one_placement[1]] += 1
        elif "remove_player" in request.form:
            removed_player = int(request.form.get("remove_player"))
            players.pop(removed_player)
        elif "delete_table" in request.form:
            players = [] 
            continue_data = None
        elif "continue" in request.form:
            chosen_league = request.form.get("league")
            chosen_gender = request.form.get("gender")
            chosen_div = request.form.get("division")
            if chosen_div == "North":
                chosen_div = 1
            elif chosen_div == "Central":
                chosen_div = 2
            elif chosen_div == "South":
                chosen_div = 3
            elif chosen_div == "Independent":
                chosen_div = 4
            if not chosen_league:
                flash("Please enter a valid league", category="error")
            elif not chosen_gender:
                flash("Please enter a valid gender", category="error")
            else: 
                chosen_sport = chosen_gender + " " + "Basketball"
                continue_data = [chosen_league, chosen_sport, int(chosen_div)]
        elif "save" in request.form:
            your_team = request.form.get("your_team")
            opponent_team = request.form.get("opponent_team")
            your_team_score = request.form.get("your_team_score")
            opponent_team_score = request.form.get("opponent_team_score")
            form_date=request.form.get("date").split("-")
            if your_team == opponent_team:
                flash("Please choose a valid opponent", category="error")
            if your_team == opponent_team:
                flash("Please choose a valid opponent", category="error")
            elif not your_team_score:
                flash("Please choose a valid score for your team", category="error")
            elif not opponent_team_score:
                flash("Please choose a valid score for your opponent's team", category="error")
            elif form_date == [" "]:
                flash("Please enter a valid date", category="error")
            else:
                python_date = date(int(form_date[0]), int(form_date[1]), int(form_date[2]))
                league_sport_division_team = continue_data[0] + " " + continue_data[1] + " " + str(continue_data[2]) + " " + request.form.get("your_team")
                existing_team = Team.query.filter_by(league_sport_division_team=league_sport_division_team).first()
                win_lose = None
                if your_team_score == opponent_team_score:
                    win_lose = 1
                    existing_team.draws += 1
                    db.session.commit()
                elif your_team_score > opponent_team_score:
                    win_lose = 2
                    existing_team.wins += 1
                    db.session.commit()
                else: 
                    win_lose = 0
                    existing_team.losses += 1
                    db.session.commit()
                add_game = Game(your_team=your_team, opponent_team=opponent_team, your_team_score=your_team_score, opponent_team_score=opponent_team_score, win_lose=win_lose, date=python_date, team_id=existing_team.id)
                db.session.add(add_game)
                db.session.commit()
                for p in players:
                    add_player = BasketballPlayerStats(num=p["Number"], name=p["Name"], field_goals = p["FG"], field_goals_attempted = p["FGA"], field_goal_percent = p["FG%"], three_pointers = p["3P"], three_pointers_attempted = p["3PA"], three_pointer_percent = p["3P%"], free_throws = p["FT"], free_throws_attempted = p["FTA"], free_throw_percent = p["FT%"], rebounds = p["TRB"], assists = p["AST"], points = p["PTS"], game_id = add_game.id)
                    db.session.add(add_player)
                db.session.commit()
                players = []
                continue_data = None
                flash('Your Stats Sheet has been saved!', category='success')
    if len(players) < 1:
        continue_data = None
    for player in range(0, len(players)):
        if players[player]["FGA"] > 0:
            players[player]["FG%"] = str(round((players[player]["FG"])/(players[player]["FGA"])*100, 2)) + "%"
        if players[player]["3PA"] > 0:
            players[player]["3P%"] = str(round((players[player]["3P"])/(players[player]["3PA"])*100, 2)) + "%"
        if players[player]["FTA"] > 0:
            players[player]["FT%"] = str(round((players[player]["FT"])/(players[player]["FTA"])*100, 2)) + "%"
    return render_template("basketballstatssheets.html", leagues=leagues, players=players, len=len(players), continue_data=continue_data, teams=teams)


@views.route("/soccerstatssheets", methods=["GET", "POST"])
def soccerstatssheets():
    global players
    global continue_data
    if request.method == "POST":
        if "add_player" in request.form:
            new_player_name = request.form.get('playername')
            new_player_number = request.form.get('playernumber')
            if not new_player_name:
                flash("Please add a name to the player", category="error")
            elif not new_player_number:
                flash("Please add a number to the player", category="error")
            else:
                players.append({"Number": new_player_number, "Name": new_player_name, "AST": 0, "Saves":0, "Shots Taken":0, "Goals": 0, "Tackles": 0, "Interceptions": 0})
        elif "add1" in request.form:
            add_one_placement = request.form.get('add1').split(", ")
            players[int(add_one_placement[0])][add_one_placement[1]] += 1
        elif "remove_player" in request.form:
            removed_player = int(request.form.get("remove_player"))
            players.pop(removed_player)
        elif "delete_table" in request.form:
            players = [] 
            continue_data = None
        elif "continue" in request.form:
            chosen_league = request.form.get("league")
            chosen_gender = request.form.get("gender")
            chosen_div = request.form.get("division")
            if chosen_div == "North":
                chosen_div = 1
            elif chosen_div == "Central":
                chosen_div = 2
            elif chosen_div == "South":
                chosen_div = 3
            elif chosen_div == "Independent":
                chosen_div = 4
            if not chosen_league:
                flash("Please enter a valid league", category="error")
            elif not chosen_gender:
                flash("Please enter a valid gender", category="error")
            else: 
                chosen_sport = chosen_gender + " " + "Soccer"
                continue_data = [chosen_league, chosen_sport, int(chosen_div)]
        elif "save" in request.form:
            your_team = request.form.get("your_team")
            opponent_team = request.form.get("opponent_team")
            your_team_score = request.form.get("your_team_score")
            opponent_team_score = request.form.get("opponent_team_score")
            form_date=request.form.get("date").split("-")
            if your_team == opponent_team:
                flash("Please choose a valid opponent", category="error")
            elif not your_team_score:
                flash("Please choose a valid score for your team", category="error")
            elif not opponent_team_score:
                flash("Please choose a valid score for your opponent's team", category="error")
            elif form_date == [" "]:
                flash("Please enter a valid date", category="error")
            else:
                python_date = date(int(form_date[0]), int(form_date[1]), int(form_date[2]))
                league_sport_division_team = continue_data[0] + " " + continue_data[1] + " " + str(continue_data[2]) + " " + request.form.get("your_team")
                existing_team = Team.query.filter_by(league_sport_division_team=league_sport_division_team).first()
                if your_team_score == opponent_team_score:
                    win_lose = 1
                    existing_team.draws += 1
                    db.session.commit()
                elif your_team_score > opponent_team_score:
                    win_lose = 2
                    existing_team.wins += 1
                    db.session.commit()
                else: 
                    win_lose = 0
                    existing_team.losses += 1
                    db.session.commit()
                add_game = Game(your_team=your_team, opponent_team=opponent_team, your_team_score=your_team_score, opponent_team_score=opponent_team_score, win_lose=win_lose, date=python_date, team_id=existing_team.id)
                db.session.add(add_game)
                db.session.commit()
                for p in players:
                    add_player = SoccerPlayerStats(num=p["Number"], name=p["Name"], assists = p["AST"], saves=p["Saves"], shots_taken=p["Shots Taken"], goals = p["Goals"], tackles = p["Tackles"], interceptions = p["Interceptions"], game_id = add_game.id)
                    db.session.add(add_player)
                db.session.commit()
                players = []
                continue_data = None
                flash('Your Stats Sheet has been saved!', category='success')
    if len(players) < 1:
        continue_data = None
    return render_template("soccerstatssheets.html", leagues=leagues, players=players, len=len(players), continue_data=continue_data, teams=teams)


@views.route("/leagues", methods=["GET", "POST"])
def view_leagues():
    global locate_stats
    if request.method == "POST":
        chosen_div = request.form.get('div_button')
        chosen_div_list = chosen_div.split(", ")
        chosen_div_list[2] = int(chosen_div_list[2])
        locate_stats[0] = chosen_div_list[0]
        locate_stats[1] = chosen_div_list[1]
        locate_stats[2] = chosen_div_list[2]
        return redirect(url_for("views.divisions", league=chosen_div_list[0], sport=chosen_div_list[1], division=chosen_div_list[2]))
    return render_template("leagues.html", leagues=leagues)


@views.route("/<league>/<sport>/<int:division>", methods=["GET", "POST"])
def divisions(league=locate_stats[0], sport=locate_stats[1], division=locate_stats[2]):
    global locate_stats
    locate_stats[0] = league
    locate_stats[1] = sport
    locate_stats[2] = division
    if request.method == "POST":
        clicked_on_team = request.form.get('team_button')
        locate_stats[3] = clicked_on_team
        return redirect(url_for("views.wantedteam", league=locate_stats[0], sport=locate_stats[1], division=locate_stats[2], team=locate_stats[3]))
    elif locate_stats:
        for lg in leagues:
            if lg.acronym == league:
                for spt in lg.sports:
                    if spt[0] == sport and 1 <= division <= spt[1]:
                        return render_template("divisions.html", leagues=leagues, league=league, sport=sport, division=division)
    abort(404)
    

@views.route("/<league>/<sport>/<int:division>/<team>", methods=["GET", "POST"])
def wantedteam(league=locate_stats[0], sport=locate_stats[1], division=locate_stats[2], team=locate_stats[3]):
    global locate_stats
    locate_stats = [league, sport, division, team, 1]
    if request.method == "POST":
        if "selected_game" in request.form:
            locate_stats[4] = int(request.form.get("selected_game"))
            return redirect(url_for("views.selectedgame", league=locate_stats[0], sport=locate_stats[1], division=locate_stats[2], team=locate_stats[3], id=locate_stats[4]))
    elif locate_stats:
        for lg in leagues:
            if lg.acronym == league:
                for spt in lg.sports:
                    if spt[0] == sport and 1 <= division <= spt[1]:
                        for tam in spt[2][division-1]:
                            if tam == team:
                                league_sport_division_team = league + " " + sport + " " + str(division) + " " + team
                                existing_team = Team.query.filter_by(league_sport_division_team=league_sport_division_team).first()
                                past_games = Game.query.filter_by(team_id=existing_team.id)
                                recorded_games = []
                                for game in past_games:
                                    format_date = str(game.date).split(" ")
                                    year_month_day = format_date[0].split("-")
                                    date = year_month_day[1] + "/" + year_month_day[2] + "/" + year_month_day[0] 
                                    recorded_games.append([date, game.your_team, game.opponent_team, game.id])
                                return render_template("teams.html", leagues=leagues, league=league, sport=sport, division=division, team=team, existing_team=existing_team, recorded_games=recorded_games)
    abort(404)


@views.route("//<league>/<sport>/<int:division>/<team>/<int:id>", methods=["GET", "POST"])
def selectedgame(league=locate_stats[0], sport=locate_stats[1], division=locate_stats[2], team=locate_stats[3], id=locate_stats[4]):
    locate_stats = [league, sport, division, team, id]
    if request.method == "POST":
        if "back" in request.form:
             return redirect(url_for("views.wantedteam", league=locate_stats[0], sport=locate_stats[1], division=locate_stats[2], team=locate_stats[3]))
    if locate_stats:
        for lg in leagues:
            if lg.acronym == league:
                for spt in lg.sports:
                    if spt[0] == sport and 1 <= division <= spt[1]:
                        for tam in spt[2][division-1]:
                            if tam == team:
                                selected_game = Game.query.filter_by(id=id).first()
                                if selected_game:
                                    format_date = str(selected_game.date).split(" ")
                                    year_month_day = format_date[0].split("-")
                                    date = year_month_day[1] + "/" + year_month_day[2] + "/" + year_month_day[0]
                                    recorded_players = None
                                    if sport == "Boys Basketball" or sport == "Girls Basketball":
                                        recorded_players = BasketballPlayerStats.query.filter_by(game_id=id)
                                    elif sport == "Boys Soccer" or sport == "Girls Soccer":
                                        recorded_players = SoccerPlayerStats.query.filter_by(game_id=id)
                                    return render_template("selectedgame.html", leagues=leagues, league=league, sport=sport, division=division, team=team, selected_game=selected_game, date=date, recorded_players=recorded_players)
    abort(404)


@views.route("/aboutus", methods=["GET", "POST"])
def aboutus():
    return render_template("aboutus.html")
