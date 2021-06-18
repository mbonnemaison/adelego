# Adelego GitHub Page

**Adelego** is a project created to help dependent people live longer and more safely at home & to improve the assistance caregivers can provide.

We created a [GitHub page](https://mbonnemaison.github.io/adelego/) with more information on the project and our vision.

### Let's work & chat together

If you want to develop this project with us, please check [our code](https://github.com/mbonnemaison/adelego/tree/master)! We're new at programming and would love your input!

If you have thoughts/ideas/suggestions on the projects, feel free to contact us on [GitHub](https://github.com/mbonnemaison) or [email us](<adele.jmb@gmail.com>).

### How to run the site locally

[Clone](https://help.github.com/en/articles/cloning-a-repository) (or [fork](https://help.github.com/en/articles/about-forks) then clone) this repo.

Install Ruby v2.6+ as explained in the [Jekyll docs](https://jekyllrb.com/docs/installation/) for your operating system (via [rbenv](https://github.com/rbenv/rbenv), for example).
If the version of ruby on your system is too recent (e.g. version 3.0.1), install Ruby Version Manager or rvm. Instructions to install rvm are [here](https://rvm.io/rvm/install) and this [youtube video](https://www.youtube.com/watch?v=cQVb7fHFjSM) details how to use rvm to install and run previous versions of ruby.

Make sure both the installed Ruby version and RubyGems are on your path:

```
$ ruby -v
$ gem -v
```

Install [Bundler](https://bundler.io/):

```
$ gem install bundler
```

Install the gems to build the site:

```
$ bundle install
```

Build and serve the site:

```
$ bundle exec jekyll serve
```

View the site in a browser at <http://localhost:4000>.

## Developing the site

This site uses the [Hydeout](https://fongandrew.github.io/hydeout/) theme. Most of the site's structure and style come from the theme.

To run Jekyll commands, use `bundle exec jekyll`.


*We thank the [Boston Python group](https://about.bostonpython.com) for allowing us to use their GitHub page as a model for our GitHub page.*
