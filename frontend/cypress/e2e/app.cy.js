describe('App E2E', () => {
  it('loads and allows typing', () => {
    cy.visit('/')
    cy.get('textarea').type('test')
  })
})
